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


def main():
    # load env vars
    logging.info("Loading env vars")
    load_dotenv()
    BOT_TOKEN = os.environ["BOT_TOKEN"]

    # define intents
    logging.info("Defining intents")
    intents = discord.Intents.default()
    # intents.members = True

    logging.info("Setting up discord client")
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        logging.info(f"Logged on as {client.user}")

    @client.event
    async def on_message(msg):
        logging.info(
            f"Message received. Author: {msg.author.id}, Channel: {msg.channel.id}"
        )

    @client.event
    async def on_raw_reaction_add(pld):
        logging.info(
            f"Reaction added. By user: {pld.user_id}, Channel: {pld.channel_id}, Emoji: {pld.emoji}"
        )

    client.run(BOT_TOKEN)


if __name__ == "__main__":
    main()
