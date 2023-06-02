from pydantic import BaseModel


#
class UserBase(BaseModel):
    username: str
    password: str
    token: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    password: str


class UserLogout(BaseModel):
    username: str
    token: str
