from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "postgresql://postgres:1234@db:5432/testdb"

engine = create_engine(DATABASE_URL)


class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(bind=engine)

