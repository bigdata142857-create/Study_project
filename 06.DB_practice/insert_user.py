from sqlalchemy.orm import Session

from database import engine
from models import User, Mentor

session = Session(engine)

# Mentor 객체 생성
mentor1 = Mentor(
    name="권효은",
    subject="ALL"
)

# 세션에 추가
session.add(mentor1)

# User 객체 생성
user1 = User(name="이용현", age=11, mentor=mentor1)
user2 = User(name="김현민", age=11, mentor=mentor1)
user3 = User(name="김서영", age=11, mentor=mentor1)
user4 = User(name="심예지", age=11, mentor=mentor1)
user5 = User(name="신상하", age=11, mentor=mentor1)
session.add_all([user1, user2, user3,user4,user5])

session.commit()
session.close()