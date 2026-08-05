from fastapi import FastAPI

from database import engine
from database import Base
from database import SessionLocal

import crud
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/users")
def create(user: schemas.UserCreate):
    db = SessionLocal()
    return crud.create_user(db, user.name, user.age)


@app.get("/users")
def read():
    db = SessionLocal()
    return crud.get_users(db)

