import uuid

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    password: str


class User(UserCreate):
    uuid: uuid.UUID


class UserFromDb(UserBase):
    uuid: uuid.UUID


class TaskBase(BaseModel):
    subject: str
    done: bool


class TaskCreate(TaskBase):
    user_uuid: uuid.UUID


class Task(TaskCreate):
    uuid: uuid.UUID


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    name: str | None = None
