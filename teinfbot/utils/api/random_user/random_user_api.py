from .random_user import User
import requests
import json
from typing import Optional
import aiohttp
import io

class RandomUserApi:
    ENDPOINT_URL = 'https://randomuser.me/api'
    @classmethod
    def get_random_user(cls) -> Optional[User]:
        resp = requests.get(cls.ENDPOINT_URL)
        if resp.ok:
            user_json = json.loads(resp.text)['results'][0]
            user = User.from_json(user_json)
            return user
    
    @classmethod
    async def get_random_user_async(cls) -> Optional[User]:
        async with aiohttp.ClientSession() as session:
            async with session.get(cls.ENDPOINT_URL) as resp:
                data = await resp.read()
                user_json = json.loads(data)['results'][0]
                user = User.from_json(user_json)
                return user
