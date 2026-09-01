import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


DATABASE_URL = os.getenv(
    "ORM_PRACTICE2_URL",
    "postgresql://postgres@localhost:5432/orm_practice2",
)
engine = create_engine(DATABASE_URL)
