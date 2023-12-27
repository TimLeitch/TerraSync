from utils.security import hash_password
from utils.db import get_db
import asyncio
import random


def generate_test_users(amount):
    # List of possible usernames (Marvel characters)
    usernames = ["ironman", "captainamerica", "blackwidow",
                 "hulk", "thor", "hawkeye", "spiderman"]
    # List of possible domains
    domains = ["starkindustries.com", "shield.gov",
               "avengers.net", "asgard.org", "webshooters.com"]
    # List of possible groups
    groups = ["admin", "super admin", "production", "sales",
              "appointment center", "manager", "director"]
    # Generate test users
    test_users = []
    for i in range(amount):  # Replace x with the number of users you want to generate
        # Append the index to the username
        username = random.choice(usernames) + str(i)
        email = f"{username}@{random.choice(domains)}"
        # Select 2 random groups for each user
        user_groups = random.sample(groups, k=2)
        test_users.append({
            "username": username,
            "email": email,
            # Hash the password
            "hashed_password": hash_password('testpassword'),
            "groups": user_groups,
        })

    # Add the premade user
    test_users.append({
        "username": "tim",
        "email": "tim@example.com",
        "hashed_password": hash_password('Passw0rd1'),
        "groups": ["super admin"],
    })

    return test_users


async def init_user(db, user_data):
    # Check if the user already exists
    existing_user = await db["users"].find_one({"username": user_data["username"]})
    # If the user already exists, delete it
    if existing_user:
        await db["users"].delete_one({"username": user_data["username"]})
    # Create the user
    await db["users"].insert_one(user_data)


async def init_db(user_data):
    async for db in get_db():
        for user in user_data:
            await init_user(db, user)


async def main():
    test_users = generate_test_users(25)
    await init_db(test_users)

# Run the init_db function
asyncio.run(main())
