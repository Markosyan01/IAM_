# CodeLab — programming lessons (React + FastAPI + MySQL)

Trilingual (Armenian / Russian / English) lessons site with photos, accounts and progress tracking.

## Run
    docker compose up --build

- Site: http://localhost:3000
- API + docs: http://localhost:8000/docs

Edit `.env` (copy of `.env.example`) before real use — change all passwords and `JWT_SECRET`.

## Structure
- `backend/` FastAPI, SQLAlchemy, JWT auth. Tables are created and seeded on first start (`app/seed.py`).
- `frontend/` React (Vite), served by nginx, which proxies `/api` to the backend.
- `docker-compose.yml` db (MySQL 8, utf8mb4, persistent volume) → backend → frontend.

## Add content
Add a course to `DATA` in `backend/app/seed.py` as (slug, photo id, level, title, description, lessons),
each text given as (en, ru, hy). Seeding only runs on an empty database, so reset with
`docker compose down -v` and start again.
Photos come from Unsplash URLs; a gradient shows if an image can't load.

## Add a language
Add `*_xx` columns in `models.py`, the code to `LANGS` in `main.py`, and a block in `frontend/src/i18n.js`.
# IAM_
# IAM_
# IAM_
