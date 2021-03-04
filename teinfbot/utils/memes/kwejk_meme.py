from __future__ import annotations

import io
from typing import List, Optional

import aiohttp
import requests
from bs4 import BeautifulSoup

from teinfbot.utils.memes import Meme


class KwejkMeme(Meme):
    KWEJK_LOSOWY_URL = "https://kwejk.pl/losowy"

    def __init__(self, title: str, url: str, image_url: str, tags: List[str]):
        super().__init__(title, url, image_url, tags)

    @classmethod
    def scrap_meme(cls, html: str) -> Optional[KwejkMeme]:
        soup = BeautifulSoup(html, 'html.parser')

        url_div = soup.find('div', class_='fb-like')
        if url_div:
            url = url_div.get('data-href')
        else:
            return None

        full_img = soup.find('img', class_='full-image')
        if full_img:
            image_url = full_img.get('src')
            title = full_img.get('alt')
        else:
            return None

        tags = []

        tag_list = soup.find('div', class_='tag-list')

        if not tag_list:
            return None

        for tag in tag_list.find_all('a'):
            tags.append(tag.text)

        meme = KwejkMeme(title, url, image_url, tags)
        return meme

    @classmethod
    def get_meme(cls, url: str) -> Optional[KwejkMeme]:
        resp = requests.get(url)
        return cls.scrap_meme(resp.text)

    @classmethod
    async def get_meme_async(cls, url: str) -> Optional[KwejkMeme]:
        async with aiohttp.ClientSession() as session:
            async with session.get(cls.KWEJK_LOSOWY_URL) as resp:
                data = io.BytesIO(await resp.read())

                return cls.scrap_meme(str(data))

    @classmethod
    def random_meme(cls) -> KwejkMeme:
        meme = cls.get_meme(cls.KWEJK_LOSOWY_URL)
        while not meme:
            meme = cls.get_meme(cls.KWEJK_LOSOWY_URL)

        return meme

    @classmethod
    async def random_meme_async(cls) -> KwejkMeme:
        meme = await cls.get_meme_async(cls.KWEJK_LOSOWY_URL)
        while not meme:
            meme = await cls.get_meme_async(cls.KWEJK_LOSOWY_URL)

        return meme
