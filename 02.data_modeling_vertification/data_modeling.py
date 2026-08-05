
# 모델링 dict
valid = {
  "order_id": 1,
  "product_name": "Keyboard",
  "quantity": 2,
  "status": "PENDING"
}
print(valid)

# 2. 모델링 dataclass
from dataclasses import dataclass

@dataclass
class Order:
    order_id: int
    product_name: str
    quantity: int
    status: str

p1 = Order(1, "Keyboard", 2, "PENDING")
p2 = Order(2, "Mouse", 1, "SHIPPED")

# 그렇다면 __eq__가 되는 보자 (잘된다)
print(p1 == p2)

# 그러면 아예 몇 개의 변수 타입을 다른 걸로 해도 작동을 할까? (잘된다)
p3 = Order('d','keyboard','4', 'PENDING')
print(p3)

# 3 Pydantic Model
from pydantic import BaseModel

# 이 class에 적혀져 있는 타입 힌트를 보고 입력값이 유효한지를 검증한다
class User(BaseModel):
    id: int
    name: str
    email: str

user = User(
    id = 145,
    name = 'jeju',
    email = 'dy14@gmail.com'
)
print(user)

# 만약 다르게 한다면
user_1 = User(
    id = '12',
    name = '123',
    email = 'dy14@gmail.com'
)
print(user_1) # 잘 출력되는 걸 볼 수 있는데 이는 (자동으로 타입을 변환해주기 때문)

from enum import Enum

class Status(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"

status = Status.PAID
print(status) # PENDING

# Optional을 활용한다면..
from typing import Optional
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    nickname: Optional[str] = None # 이 닉네임은 필수 입력값이 아님!!

# 예
user = User(
    id = 145,
    name = "maplestory!!",
    email = "john.doe@example.com"
)

print(user)

# 닉네임을 쓴다면?
user_with_nickname = User(
    id = 146,
    name = "-메-",
    email = "adventure@example.com",
    nickname = "-메플-"
)

print(user_with_nickname)


