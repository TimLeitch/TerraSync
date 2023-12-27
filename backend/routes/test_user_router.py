import pytest
from httpx import AsyncClient
from fastapi import FastAPI, APIRouter
from pymongo import MongoClient
from routes.user_router import router as user_router


@pytest.fixture
def test_app():
    # Create a test version of the FastAPI app
    app = FastAPI()
    app.include_router(user_router)

    return app


@pytest.fixture
async def test_db():
    # Connect to a test database
    client = MongoClient("mongodb://localhost:27017")
    db = client["test_db"]

    # Create a test collection for users
    db["users"].drop()
    db["users"].insert_one({
        "username": "existing_user",
        "email": "existing_user@example.com",
        "hashed_password": "hashed_password"
    })

    yield db

    # Clean up the test database
    db["users"].drop()
    client.close()


@pytest.mark.asyncio
async def test_register_user_existing_user(test_app):
    # Create a test client
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        # Send a request to register an existing user
        response = await client.post("/register", json={
            "username": "existing_user",
            "email": "existing_user@example.com",
            "password": "password"
        })

        # Check that the response has a status code of 400
        assert response.status_code == 400

        # Check that the response contains the correct error message
        assert response.json() == {"detail": "Username already exists"}


@pytest.mark.asyncio
async def test_register_user_new_user(test_app):
    # Create a test client
    async with AsyncClient(app=test_app, base_url="http://test") as client:
        # Send a request to register a new user
        response = await client.post("/register", json={
            "username": "new_user",
            "email": "new_user@example.com",
            "password": "password"
        })

        # Check that the response has a status code of 200
        assert response.status_code == 200

        # Check that the response contains the correct user data
        assert response.json() == {"username": "new_user",
                                   "email": "new_user@example.com"}
