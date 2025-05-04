import os
from pymongo.errors import ConnectionFailure
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI") or "mongodb://mongo:password@localhost:27017"
MONGO_DB = os.getenv("MONGO_DB") or "teinf"

client = AsyncIOMotorClient(MONGO_URI)
try:
    client.admin.command("ping")
    print("✅ MongoDB connection successful.")
except ConnectionFailure:
    print("❌ MongoDB connection failed.")

db = client.get_database(MONGO_DB)
