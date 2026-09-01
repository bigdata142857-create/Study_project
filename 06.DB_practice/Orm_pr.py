import os

from sqlalchemy import Integer, String, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column


class Base(DeclarativeBase):
    pass


DATABASE_URL = os.getenv(
    "ORM_PRACTICE_URL",
    "postgresql://postgres@localhost:5432/orm_practice",
)
engine = create_engine(DATABASE_URL)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40))
    age: Mapped[int] = mapped_column(Integer)


Base.metadata.create_all(engine)

session = Session(engine)

user1 = User(name="이용현", age=25)
user2 = User(name="김현민", age=24)
user3 = User(name="김서영", age=23)
user4 = User(name="신상하", age=26)
user5 = User(name="심예지", age=30)

session.add_all([user1, user2, user3, user4, user5])
session.commit()

stmt = select(User)
users = session.scalars(stmt).all()

for user in users:
    print(user.id, user.name, user.age)

stmt = select(User).where(User.name == "이용현")
user = session.scalar(stmt)

if user is not None:
    print(user.id)
    print(user.age)

session.close()
