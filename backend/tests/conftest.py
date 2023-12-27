import pytest
import asyncio
from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from main import app, get_db
from utils.security import hash_password

client = TestClient(app)

# Database URL for testing
TEST_DATABASE_URL = "mongodb://localhost:27017/test_db"

print("Connecting to MongoDB")


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
async def db():
    client = AsyncIOMotorClient(TEST_DATABASE_URL)
    db = client.get_database("test_db")  # Specify the database name here
    yield db
    client.close()


@pytest.fixture(autouse=True, scope="function")
async def create_test_user(db):
    print("Creating test user")
    user_data = {
        "username": "testuser",
        "email": "testuser@example.com",
        "password": "testpassword"
    }
    user_data["password"] = hash_password("testpassword")
    print(user_data)
    await db["users"].insert_one(user_data)
    yield
    await db["users"].delete_one({"username": "testuser"})
