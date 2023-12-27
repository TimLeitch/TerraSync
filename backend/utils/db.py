from motor.motor_asyncio import AsyncIOMotorClient


async def get_db():
    print("Connecting to MongoDB")
    client = AsyncIOMotorClient("mongodb://localhost:27017")  # Local docker
    # client = AsyncIOMotorClient("mongodb://mongo:27017") # Docker-compose
    db = client.get_database("test_db")
    print(f"Connected to database: {db.name}")
    try:
        yield db
    finally:
        print("Closing MongoDB connection")
        client.close()
