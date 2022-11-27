import uuid
from datetime import timedelta
from functools import lru_cache
from typing import List

from auth import (ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token, get_current_user,
                  get_password_hash)
from config import Settings
from database import database, tasks, users
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from schemas import Task, TaskCreate, Token, User, UserCreate, UserFromDb


@lru_cache()
def get_settings():
    return Settings()


app = FastAPI()

origins = [
    "http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.post("/token", response_model=Token)
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


@app.get("/tasks/", response_model=List[Task])
async def read_tasks(_: User = Depends(get_current_user)):
    query = tasks.select()
    return await database.fetch_all(query)


@app.post("/tasks/", response_model=Task)
async def create_task(task: TaskCreate, _: User = Depends(get_current_user)):
    task_uuid = uuid.uuid4()
    query = tasks.insert().values(uuid=task_uuid, **task.dict())
    _ = await database.execute(query)
    return {**task.dict(), "uuid": task_uuid}


@app.get("/users/", response_model=List[UserFromDb])
async def read_users(_: User = Depends(get_current_user)):
    query = users.select()
    return await database.fetch_all(query)


@app.post("/users/", response_model=UserFromDb)
async def create_user(user: UserCreate):
    user_uuid = uuid.uuid4()
    hashed_password = get_password_hash(user.dict()["password"])
    query = users.insert().values(uuid=user_uuid, name=user.dict()["name"], password=hashed_password)
    _ = await database.execute(query)
    return {**user.dict(), "uuid": user_uuid}
