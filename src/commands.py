import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[logging.StreamHandler()],
)

CHANNEL_IDS = [""]
AUTHORISED_USER_IDS = [123]

def check_auth(ctx):
    """
    Check if the command is triggered by an authorised user.
    """
    return ctx.message.author.id in AUTHORISED_USER_IDS

def main():
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
    async def channels(ctx):
        logging.info(f"Command triggered. Name:channels, Author: {ctx.author.id}, Channel: {ctx.channel.id}")
        counter = 0
        async for message in ctx.channel.history(limit=200):
            counter += 1
        await ctx.send(f"Found a total of {counter} messages.")

    

    bot.run(BOT_TOKEN)


if __name__ == "__main__":
    main()
