from __future__ import annotations

from typing import List

import discord


class Meme:
    def __init__(self, title: str, url: str, image_url: str, tags: List[str]):
        self.title = title
        self.url = url
        self.image_url = image_url
        self.tags = tags

    @property
    def embed(self) -> discord.Embed:
        em = discord.Embed(title=self.title)
        em.set_image(url=self.image_url)
        em.add_field(name="URL", value=self.url)
        em.set_footer(text=" ".join(self.tags))

        return em
