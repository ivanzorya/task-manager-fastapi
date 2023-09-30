import pytest_asyncio
from httpx import AsyncClient
from src.database import database, tasks, users

from app.main import app


async def clean_test_db():
    query = tasks.delete()
    await database.execute(query)

    query = users.delete()
    await database.execute(query)


@pytest_asyncio.fixture(autouse=True)
async def db_connect():
    await database.connect()
    yield

    await clean_test_db()

    await database.disconnect()


@pytest_asyncio.fixture()
async def async_test_client():
    async with AsyncClient(
        app=app,
        base_url="http://localhost:8000",
        headers={"Content-Type": "application/json"},
    ) as ac:
        yield ac
