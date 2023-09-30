import uuid
from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_password_hash,
)
from src.database import database, tasks, users
from src.schemas import Task, TaskCreate, Token, User, UserCreate, UserFromDb


router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.name}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/tasks/", response_model=List[Task])
async def read_tasks(_: User = Depends(get_current_user)):
    query = tasks.select()
    return await database.fetch_all(query)


@router.post("/tasks/", response_model=Task)
async def create_task(task: TaskCreate, _: User = Depends(get_current_user)):
    task_uuid = uuid.uuid4()
    query = tasks.insert().values(uuid=task_uuid, **task.model_dump())
    _ = await database.execute(query)
    return {**task.model_dump(), "uuid": task_uuid}


@router.get("/users/", response_model=List[UserFromDb])
# async def read_users(_: User = Depends(get_current_user)):
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@router.post("/users/", response_model=UserFromDb)
async def create_user(user: UserCreate):
    user_uuid = uuid.uuid4()
    hashed_password = get_password_hash(user.model_dump()["password"])
    query = users.insert().values(uuid=user_uuid, name=user.model_dump()["name"], password=hashed_password)
    _ = await database.execute(query)
    return {**user.model_dump(), "uuid": user_uuid}
