from __future__ import annotations
from youtube_dl import YoutubeDL
import io
import aiohttp
from typing import Optional


class MusicVideo:
    def __init__(self, title: str, source: str, thumbnail: str, webpage: str):
        self.title = title
        self.source = source
        self.thumbnail = thumbnail
        self.webpage = webpage

    @classmethod
    async def get(cls, url: str) -> Optional[MusicVideo]:
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': 'True',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with YoutubeDL(ydl_opts) as ydl:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        pass
            except:
                info = ydl.extract_info(f"ytsearch:{url}", download=False)[
                    'entries'][0]
            else:
                info = ydl.extract_info(url, download=False)

        try:
            return MusicVideo(
                info['title'],
                info['formats'][0]['url'],
                info['thumbnail'],
                info['webpage_url']
            )
        except:
            return None
