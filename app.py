import os
import string
import requests

import discord
import dotenv
import re

from catbox_api import catboxAPI

import random

assert dotenv.load_dotenv()
token = str(os.getenv("TOKEN"))
catbox_token = str(os.getenv("CATBOX_USERHASH"))

bot = discord.Bot()

catbox_api = catboxAPI(catbox_token)

CATBOX_ALBUM_ID = "slq44d"

# from https://github.com/tikendraw/catsay/blob/main/catsay/cat.py
def catsay(input_string: str):
    """make a cat say anything you pass"""

    length = len(input_string) + 2

    cat_message = f"""
```
           {"-" * length}
          ( {input_string} )
           {"-" * length}
          |/
    /\\_/\\
   ( o.o )
    > ^ <  ,"",
    ( " ) :
     (|)""
```
      """

    return cat_message

def get_album_files(album_id):
    response = requests.get(f"https://catbox.moe/c/{album_id}")
    urls = re.findall(r"<a href='(.*?)' target='_blank'>", response.text)

    return urls

def get_cat_image():
    images = get_album_files(CATBOX_ALBUM_ID)

    return random.choice(images)

def add_cat_image(image_url):
    file_ref = catbox_api.upload_from_url(image_url)
    # return catbox_api.upload_file_to_album(CATBOX_ALBUM_ID, "image.png", image)
    catbox_api.add_file_to_album(CATBOX_ALBUM_ID, file_ref)

    return file_ref

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


@bot.slash_command(
    name="ping",
    description="test if the bot can respond",
    integration_types={
        discord.IntegrationType.user_install,
    },
)
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond(f"pong! latency is {bot.latency}ms :3")


@bot.slash_command(
    name="catsay",
    description="say as a cat!!",
    integration_types={
        discord.IntegrationType.user_install,
    },
)
async def catsay_cmd(ctx: discord.ApplicationContext, text: str):
    await ctx.respond(catsay(text))

@bot.slash_command(
    name = "silly_cat",
    description = "get a silly cat image!! :3",
    integration_types={
        discord.IntegrationType.user_install,
    },
)
async def silly_cat(ctx: discord.ApplicationContext):
    embed = discord.Embed(
        title="kitty!!!!",
        color=discord.Colour.blurple(),
    )

    embed.set_image(url=get_cat_image())

    await ctx.respond(embed=embed)

@bot.slash_command(
    name = "upload_silly",
    description = "(reserved for admins)",
    integration_types = {
        discord.IntegrationType.user_install,
    }
)
async def upload_silly(ctx: discord.ApplicationContext, file: discord.Option(discord.Attachment, "the silly cat image")):
    if ctx.author.name != "colonthreeing":
        await ctx.respond(
            "you are not allowed to use this command!",
            ephemeral = True
        )
        return
    if not file.content_type.startswith("image"):
        await ctx.respond(
            f"that's not an image! (submitted a {file.content_type})",
            ephemeral = True
        )
        return

    url = add_cat_image(file.url)

    await ctx.respond(
        f"Uploaded image to {url}",
        ephemeral = True
    )

bot.run(token)
