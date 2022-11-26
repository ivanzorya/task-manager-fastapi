import uuid
from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI
from schemas import Task, TaskCreate, User, UserCreate
from sqlalchemy.dialects.postgresql import UUID

DATABASE_URL = "postgresql://postgres:postgres@db/postgres"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

tasks = sqlalchemy.Table(
    "task",
    metadata,
    sqlalchemy.Column("uuid", UUID, primary_key=True),
    sqlalchemy.Column("user_uuid", UUID, sqlalchemy.ForeignKey("user.uuid")),
    sqlalchemy.Column("subject", sqlalchemy.String),
    sqlalchemy.Column("done", sqlalchemy.Boolean),
)

users = sqlalchemy.Table(
    "user",
    metadata,
    sqlalchemy.Column("uuid", UUID, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
)


engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)


app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/tasks/", response_model=List[Task])
async def read_tasks():
    query = tasks.select()
    return await database.fetch_all(query)


@app.post("/tasks/", response_model=Task)
async def create_task(task: TaskCreate):
    task_uuid = uuid.uuid4()
    query = tasks.insert().values(uuid=task_uuid, **task.dict())
    _ = await database.execute(query)
    return {**task.dict(), "uuid": task_uuid}


@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    user_uuid = uuid.uuid4()
    query = users.insert().values(uuid=user_uuid, **user.dict())
    _ = await database.execute(query)
    return {**user.dict(), "uuid": user_uuid}
