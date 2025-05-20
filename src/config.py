import os
from dataclasses import dataclass, field


def getenv(key: str, default=None, cast_type=str):
    val = os.getenv(key, default)
    try:
        return cast_type(val)
    except (ValueError, TypeError):
        return default


@dataclass
class DatabaseConfig:
    url: str = getenv("DB__URL", "mongodb://mongo:password@localhost:27017")
    name: str = getenv("DB__NAME", "teinf")


@dataclass
class DiscordConfig:
    guild_id: int = getenv("DC__GUILD_ID", 406476256646004736, int)
    afk_channel_id: int = getenv("DC__AFK_CHANNEL_ID", 423934688244006913, int)
    random_nickname_user_id: int = getenv(
        "DC__RANDOM_NICKNAME_USER_ID", 239329824361938944, int
    )
    random_nickname_channel_id: int = getenv(
        "DC__RANDOM_NICKNAME_CHANNEL_ID", 720628646267584572, int
    )


@dataclass
class BotConfig:
    access_token: str = getenv("BOT__ACCESS_TOKEN")


@dataclass
class Config:
    db: DatabaseConfig = field(default_factory=DatabaseConfig)
    dc: DiscordConfig = field(default_factory=DiscordConfig)
    bot: BotConfig = field(default_factory=BotConfig)


config = Config()
