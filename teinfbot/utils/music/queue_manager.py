from teinfbot.bot import TeinfBot
from teinfbot.utils.music import MusicVideo
from typing import List


class QueueManager:
    queue: List[MusicVideo] = []

    def __init__(self, bot: TeinfBot):
        self.bot = bot

    def add(self, video: MusicVideo):
        self.queue.append(video)

    def clear(self):
        self.queue = []

    def get_next(self):
        if len(self.queue) > 1:
            self.queue.pop(0)
            return self.queue[0]
        if len(self.queue) == 1:
            self.queue.pop(0)

        return None