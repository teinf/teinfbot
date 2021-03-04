from __future__ import annotations

import io
import random
from typing import List, Optional

import aiohttp
import requests
from bs4 import BeautifulSoup

from teinfbot.utils.memes import Meme


class JbzdMeme(Meme):
    def __init__(self, title: str, url: str, image_url: str, tags: List[str]):
        super().__init__(title, url, image_url, tags)

    @classmethod
    def scrap_meme(cls, html: str) -> Optional[JbzdMeme]:
        soup = BeautifulSoup(html, "html.parser")

        tags = []
        for tag in soup.find_all('a', class_='article-tag'):
            tags.append(tag.text)

        if soup.find('img', class_='article-image'):
            # zdjęcie
            image_url = soup.find('img', class_='article-image')['src']
        elif soup.find('video', class_='video-js'):
            # film
            image_url = soup.find('video', class_='video-js').source['src']

        else:
            return None

        title = soup.find('h3', class_='article-title').a.text.lstrip().rstrip()

        url = soup.find('h3', class_='article-title').a['href']

        meme = JbzdMeme(title, url, image_url, tags)

        return meme

    @classmethod
    def scrap_memes(cls, html: str) -> List[JbzdMeme]:
        memes: List[JbzdMeme] = []

        soup = BeautifulSoup(html, 'html.parser')

        articles = soup.findAll('article', class_='article')

        for article in articles:
            meme = cls.scrap_meme(str(article))

            if meme:
                memes.append(meme)

        return memes

    @classmethod
    def get_meme(cls, url: str) -> JbzdMeme:
        data = requests.get(url)
        return cls.scrap_meme(data.text)

    @classmethod
    async def get_meme_async(cls, url: str) -> JbzdMeme:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = io.BytesIO(await resp.read())

                meme = cls.scrap_meme(str(data))
                return meme

    @classmethod
    def random_meme(cls) -> JbzdMeme:

        page = random.randint(1, 200)

        url = f'https://jbzd.com.pl/str/{page}'

        data = requests.get(url)
        memes = cls.scrap_memes(data.text)

        return random.choice(memes)

    @classmethod
    async def random_meme_async(cls) -> JbzdMeme:

        page = random.randint(1, 200)

        url = f'https://jbzd.com.pl/str/{page}'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = io.BytesIO(await resp.read())

                return random.choice(cls.scrap_memes(str(data)))
