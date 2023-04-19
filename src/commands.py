import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import yaml

# logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[logging.StreamHandler()],
)

# load config
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)
CHANNEL_IDS = config["social_engagement"]["channels_tracked"]["ids"]
AUTHORISED_USER_IDS = config["auth"]["authorised_users"]["ids"]


def check_auth(ctx):
    """
    Check if the command is triggered by an authorised user.
    """
    return ctx.message.author.id in AUTHORISED_USER_IDS

# load env vars
logging.info("Loading env vars")
load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]

# define intents
logging.info("Defining intents")
intents = discord.Intents.default()
intents.message_content = True

logging.info("Setting up discord bot")
bot = commands.Bot(command_prefix='$', intents=intents)

def main():
    @bot.command()
    async def test(ctx):
        logging.info(f"Command triggered. Name:test, Author: {ctx.author.id}, Channel: {ctx.channel.id}")
        await ctx.send("Hello. This bot is working 👌")

    @bot.command()
    @commands.check(check_auth)
    async def auth(ctx):
        logging.info(f"Command triggered. Name:auth, Author: {ctx.author.id}, Channel: {ctx.channel.id}")
        await ctx.send("You are authorised ✅")

    @bot.command()
    async def get_hist(ctx):
        logging.info(f"Command triggered. Name:get_hist, Author: {ctx.author.id}, Channel: {ctx.channel.id}")
        counter = 0
        async for message in ctx.channel.history(limit=200):
            counter += 1
        await ctx.send(f"Found a total of {counter} messages.")

    @bot.command()
    async def file(ctx):
        logging.info(f"Command triggered. Name:file, Author: {ctx.author.id}, Channel: {ctx.channel.id}")
        file_path = "./data/att.csv"
        logging.info(f"Attaching file: {file_path}")
        file = discord.File(file_path)
        await ctx.send(file=file, content=f"Here is a file.")

    @bot.command()
    async def ch(ctx):
        logging.info(f"Command triggered. Name:ch, Author: {ctx.author.id}, Channel: {ctx.channel.id}")
        channels = []
        for channel_id in CHANNEL_IDS:
            channels.append(bot.get_channel(channel_id))
        try:
            channel_names = [c.name for c in channels]
            await ctx.send(f"Channel names: {channel_names}")
        except Exception as ex:
            logging.error(ex)


    bot.run(BOT_TOKEN)


if __name__ == "__main__":
    main()
