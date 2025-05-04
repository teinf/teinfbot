from .client import db
from dataclasses import dataclass
from typing import Optional


@dataclass
class UserModel:
    discord_id: int

    _id: Optional[str] = None
    time_spent: int = 0


user_collection = db.get_collection("users")


class User:
    @staticmethod
    async def create(user_data: UserModel):
        user_dict = user_data.__dict__.copy()
        user_dict.pop("_id", None)  # Remove _id if present
        result = await user_collection.insert_one(user_dict)
        user_data._id = result.inserted_id

    @staticmethod
    async def _find_or_create(discord_id: int) -> UserModel:
        data = await User._find(discord_id)
        if data is None:
            await User.create(UserModel(discord_id=discord_id))
        return await User._find(discord_id)

    @staticmethod
    async def _find(discord_id: int) -> Optional[UserModel]:
        data = await user_collection.find_one({"discord_id": discord_id})
        if data is None:
            return None

        return UserModel(**data)

    @staticmethod
    async def find(discord_id: int) -> UserModel:
        return await User._find_or_create(discord_id)

    @staticmethod
    async def get_top_time_spent(limit=10) -> list[UserModel]:
        cursor = user_collection.find().sort("time_spent", -1).limit(limit)
        results = await cursor.to_list(length=limit)
        return [UserModel(**user) for user in results]

    @staticmethod
    async def increment_time(discord_ids: list[int], amount: int):
        if not discord_ids:
            return

        await user_collection.update_many(
            {"discord_id": {"$in": discord_ids}}, {"$inc": {"time_spent": amount}}
        )
