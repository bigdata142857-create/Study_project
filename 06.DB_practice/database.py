from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

# Base 생성
class Base(DeclarativeBase):
    pass

# DB 연결
engine = create_engine(
    "postgresql://postgres:3822@localhost:5432/orm_practice2"
)