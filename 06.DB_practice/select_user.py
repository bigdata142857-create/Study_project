from sqlalchemy.orm import Session
from sqlalchemy import select

from database import engine
from models import Mentor
from models import User

session = Session(engine)   # 세션 객체 생성

# 실제 관계가 잘 생성되었는지
user = session.scalar(select(User).where(User.name == "이용현"))

print(user.mentor.name)
print(user.mentor.subject)

session.close()