from sqlalchemy import create_engine
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import Session
from sqlalchemy import select

# 부모 클래스(Base) 생성
# 여기에 모든 모델이 공통으로 사용할 설정을 넣기도 가능함!
class Base(DeclarativeBase):
    pass

# 실제 DB 연결
engine = create_engine(
    "postgresql://postgres:3822@localhost:5432/orm_practice"
)

# Users 테이블 생성
class User(Base):
    __tablename__ = "users"

    # pk 및 다른 값들 설정
    id: Mapped[int] = mapped_column(primary_key = True)
    name: Mapped[str] = mapped_column(String(40))
    age: Mapped[int] = mapped_column(Integer)

# 실제로 데이터베이스를 넣는 코드
Base.metadata.create_all(engine)

# 세션 생성 (세션을 생성해야 값을 넣을 수 있다)
session = Session(engine)

# User 테이블에 넣고 싶은 값
# 이런 것들이 다 하나의 객체이기에 속성에 접근하기가 가능한 것
user1 = User(name="이용현", age=25)
user2 = User(name="김현민", age=24)
user3 = User(name="김서영", age=23)
user4 = User(name="신상하", age=26)
user5 = User(name="심예지", age=30)

# 한꺼번에 저장
session.add_all([user1,user2,user3,user4,user5])

# commit
session.commit()

# 조회 방법
stm = select(User) # SQL로 따지면 모든 사람 검색 조회 Select *
# 조회 결과를 유저 객체 리스트로 가져오기
users = session.scalars(stm).all()

# 이걸 출력한다면 전체가 나온다
for user in users:
    print(user.id, user.name, user.age)

# 어떤 조건을 달고 조회를 하려고 한다면
stmt = select(User).where(User.name == "이용현")

user = session.scalar(stmt)

print(user.id)
print(user.age)

'''
# 자동으로 생성되는 지 확인용
print(user1.id)
print(user2.id)
print(user3.id)
print(user4.id)
print(user5.id)
'''
# 세션 종료
session.close()

