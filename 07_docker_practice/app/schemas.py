from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    age: int


class UserResponse(UserCreate):
    id: int

    class Config:
        from_attributes = True