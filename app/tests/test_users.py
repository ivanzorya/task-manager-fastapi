import json

import pytest


@pytest.mark.asyncio
async def test_users(async_test_client):
    response = await async_test_client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 0

    response = await async_test_client.post(
        "/users/", content=json.dumps({"name": "test_name", "password": "test_password"})
    )
    assert response.status_code == 200
    user_uuid = response.json()["uuid"]

    response = await async_test_client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["uuid"] == user_uuid
