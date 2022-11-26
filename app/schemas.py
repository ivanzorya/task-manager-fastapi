import uuid

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    pass


class User(UserCreate):
    uuid: uuid.UUID

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    subject: str
    done: bool


class TaskCreate(TaskBase):
    user_uuid: uuid.UUID


class Task(TaskCreate):
    uuid: uuid.UUID

    class Config:
        orm_mode = True
