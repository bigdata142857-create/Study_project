from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40))
    age: Mapped[int] = mapped_column(Integer)
    
    mentor_id: Mapped[int] = mapped_column(ForeignKey("mentors.id"))
    # User가 어떤 Mentor를 가지는지
    mentor: Mapped["Mentor"] = relationship(back_populates="users")

class Mentor(Base):
    __tablename__ = "mentors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40))
    subject: Mapped[str] = mapped_column(String(30))

    # Mentor가 담당하는 User 목록
    users: Mapped[list["User"]] = relationship(back_populates="mentor")