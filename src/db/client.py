from pymongo.errors import ConnectionFailure
from motor.motor_asyncio import AsyncIOMotorClient
from config import config

client = AsyncIOMotorClient(config.db.url)
try:
    client.admin.command("ping")
    print("✅ MongoDB connection successful.")
except ConnectionFailure:
    print("❌ MongoDB connection failed.")

db = client.get_database(config.db.name)
