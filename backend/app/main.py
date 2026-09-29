import os, time, hmac, hashlib, secrets
from datetime import datetime, timedelta, timezone
from contextlib import asynccontextmanager
import jwt
from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .db import Base, engine, SessionLocal, get_db
from .models import User, Course, Lesson, Progress
from .seed import seed

SECRET = os.environ["JWT_SECRET"]
LANGS = ("en", "ru", "hy")


@asynccontextmanager
async def lifespan(app):
    for _ in range(30):  # wait for MySQL
        try:
            Base.metadata.create_all(engine)
            break
        except Exception:
            time.sleep(2)
    with SessionLocal() as db:
        seed(db)
    yield


app = FastAPI(title="CodeLab API", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


def tr(obj, field, lang):
    lang = lang if lang in LANGS else "en"
    return getattr(obj, f"{field}_{lang}") or getattr(obj, f"{field}_en")


def hash_pw(pw, salt=None):
    salt = salt or secrets.token_hex(8)
    h = hashlib.pbkdf2_hmac("sha256", pw.encode(), salt.encode(), 200_000).hex()
    return f"{salt}${h}"


def check_pw(pw, stored):
    salt, _ = stored.split("$")
    return hmac.compare_digest(hash_pw(pw, salt), stored)


def make_token(user):
    exp = datetime.now(timezone.utc) + timedelta(days=7)
    return jwt.encode({"sub": str(user.id), "exp": exp}, SECRET, algorithm="HS256")


def optional_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        return None
    try:
        data = jwt.decode(authorization[7:], SECRET, algorithms=["HS256"])
        return db.get(User, int(data["sub"]))
    except Exception:
        return None


def required_user(user=Depends(optional_user)):
    if not user:
        raise HTTPException(401, "Not authenticated")
    return user


def done_ids(db, user):
    if not user:
        return set()
    return {p.lesson_id for p in db.query(Progress).filter_by(user_id=user.id)}


class Register(BaseModel):
    name: str
    email: str
    password: str


class Login(BaseModel):
    email: str
    password: str


@app.post("/api/auth/register")
def register(b: Register, db: Session = Depends(get_db)):
    email = b.email.strip().lower()
    if "@" not in email or len(b.password) < 6 or not b.name.strip():
        raise HTTPException(422, "invalid_input")
    if db.query(User).filter_by(email=email).first():
        raise HTTPException(409, "email_taken")
    u = User(email=email, name=b.name.strip(), password_hash=hash_pw(b.password))
    db.add(u); db.commit()
    return {"token": make_token(u), "user": {"name": u.name, "email": u.email}}


@app.post("/api/auth/login")
def login(b: Login, db: Session = Depends(get_db)):
    u = db.query(User).filter_by(email=b.email.strip().lower()).first()
    if not u or not check_pw(b.password, u.password_hash):
        raise HTTPException(401, "bad_credentials")
    return {"token": make_token(u), "user": {"name": u.name, "email": u.email}}


@app.get("/api/me")
def me(u=Depends(required_user)):
    return {"name": u.name, "email": u.email}


@app.get("/api/courses")
def courses(lang: str = "en", db: Session = Depends(get_db), user=Depends(optional_user)):
    done = done_ids(db, user)
    return [{"slug": c.slug, "image": c.image, "level": c.level,
             "title": tr(c, "title", lang), "description": tr(c, "desc", lang),
             "lesson_count": len(c.lessons),
             "done": sum(1 for l in c.lessons if l.id in done)}
            for c in db.query(Course).order_by(Course.id)]


@app.get("/api/courses/{slug}")
def course(slug: str, lang: str = "en", db: Session = Depends(get_db), user=Depends(optional_user)):
    c = db.query(Course).filter_by(slug=slug).first()
    if not c:
        raise HTTPException(404, "not_found")
    done = done_ids(db, user)
    return {"slug": c.slug, "image": c.image, "level": c.level,
            "title": tr(c, "title", lang), "description": tr(c, "desc", lang),
            "lessons": [{"id": l.id, "position": l.position, "title": tr(l, "title", lang),
                         "done": l.id in done} for l in c.lessons]}


@app.get("/api/lessons/{lesson_id}")
def lesson(lesson_id: int, lang: str = "en", db: Session = Depends(get_db), user=Depends(optional_user)):
    l = db.get(Lesson, lesson_id)
    if not l:
        raise HTTPException(404, "not_found")
    sib = l.course.lessons
    i = sib.index(l)
    return {"id": l.id, "course_slug": l.course.slug, "course_title": tr(l.course, "title", lang),
            "position": l.position, "title": tr(l, "title", lang), "body": tr(l, "body", lang),
            "code": l.code, "prev_id": sib[i - 1].id if i > 0 else None,
            "next_id": sib[i + 1].id if i < len(sib) - 1 else None,
            "done": l.id in done_ids(db, user)}


@app.post("/api/lessons/{lesson_id}/complete")
def complete(lesson_id: int, db: Session = Depends(get_db), u=Depends(required_user)):
    if not db.get(Lesson, lesson_id):
        raise HTTPException(404, "not_found")
    if not db.query(Progress).filter_by(user_id=u.id, lesson_id=lesson_id).first():
        db.add(Progress(user_id=u.id, lesson_id=lesson_id)); db.commit()
    return {"done": True}


@app.delete("/api/lessons/{lesson_id}/complete")
def uncomplete(lesson_id: int, db: Session = Depends(get_db), u=Depends(required_user)):
    db.query(Progress).filter_by(user_id=u.id, lesson_id=lesson_id).delete()
    db.commit()
    return {"done": False}
