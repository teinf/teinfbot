from __future__ import annotations
import discord
import random
import aiohttp
from bs4 import BeautifulSoup
import io
import requests

class Meme:
    def __init__(self, title: str, url: str , image_url: str, tags: List[str], votes: int):
        self.title = title
        self.url = url
        self.image_url = image_url
        self.tags = tags
        self.votes = votes

    @property
    def embed(self) -> discord.Embed:
        em = discord.Embed(title=self.title)
        em.set_image(url=self.image_url)
        
        em.add_field(
            name="URL",
            value=self.url
        )

        em.set_footer(
            text=" ".join(self.tags)
        )

        return em

    @staticmethod
    def parse_meme(html: str) ->  Meme:
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
            with open('x.html', 'w') as f:
                f.write(html)
            return None

        votes = int(soup.find('vote')[':score'])

        title = soup.find('h3', class_='article-title').a.text.lstrip().rstrip()

        url = soup.find('h3', class_='article-title').a['href']

        meme = Meme(title, url, image_url, tags, votes)

        return meme
    
    @staticmethod
    def parse_memes(html: str) -> List[Meme]:
        memes: List[Meme] = []

        soup = BeautifulSoup(html, 'html.parser')

        articles = soup.findAll('article', class_='article')

        for article in articles:
            meme = Meme.parse_meme(str(article))

            if meme:
                memes.append(meme)
        
        return memes

    @staticmethod
    def get_meme(url: str) -> Meme:
        data = requests.get(url)
        return Meme.parse_meme(data.text)

    @staticmethod
    async def get_meme_async(url: str) -> Meme:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = io.BytesIO(await resp.read())

                meme = Meme.parse_meme(data)
                return meme


    @staticmethod
    def random_meme(page: int = None) -> Meme:

        if not page:
            page = random.randint(1, 200)

        url = f'https://jbzd.com.pl/str/{page}'

        data = requests.get(url)
        memes = Meme.parse_memes(data.text)

        return random.choice(memes)

    @staticmethod
    async def random_meme_async(page: int = None) -> Meme:

        if not page:
            page = random.randint(1, 200)

        url = f'https://jbzd.com.pl/str/{page}'


        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = io.BytesIO(await resp.read())

                return random.choice(Meme.parse_memes(data))

