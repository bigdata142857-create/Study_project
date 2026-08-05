from sqlalchemy.orm import Session

from models import User


def create_user(db: Session, name: str, age: int):

    user = User(name=name, age=age)

    db.add(user)

    db.commit()

    db.refresh(user)

    return user


def get_users(db: Session):

    return db.query(User).all()