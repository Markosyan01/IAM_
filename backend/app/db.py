import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

URL = "mysql+pymysql://{u}:{p}@{h}:3306/{d}?charset=utf8mb4".format(
    u=os.environ["DB_USER"], p=os.environ["DB_PASSWORD"],
    h=os.environ.get("DB_HOST", "db"), d=os.environ["DB_NAME"])
engine = create_engine(URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
