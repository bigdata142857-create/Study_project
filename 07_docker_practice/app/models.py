from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database import Base


class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str]

    age: Mapped[int]