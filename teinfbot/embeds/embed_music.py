import discord


def embed_add_to_queue(title: str, webpage, thumbnail: str) -> discord.Embed:
    em = discord.Embed(
        title="MUSIC BOT",
        description=f"Dodano {title} do kolejki\n{webpage}",
        color=discord.Colour.gold()
    )

    em.set_image(url=thumbnail)

    return em


def embed_playing(title: str, webpage, thumbnail: str) -> discord.Embed:
    em = discord.Embed(
        title="MUSIC BOT",
        description=f"Odtwarzam {title}\n{webpage}",
        color=discord.Colour.green()
    )
    em.set_image(url=thumbnail)
