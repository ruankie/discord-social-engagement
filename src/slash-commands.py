# based on https://www.linkedin.com/pulse/discord-bot-part-2-slash-commands-leandro-fumio-kino
# check this out next: https://www.youtube.com/watch?v=jh1CtQW4DTo

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import yaml
from datetime import datetime
from src.utils import (
    HistoricalDiscordMessage, 
    hist_msg_list_to_pandas_df, 
    summarise_counts_by_group_and_freq, 
    summarise_counts,
    get_hist_summary_discord_embed
)

# logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s]: %(message)s",
    handlers=[logging.StreamHandler()],
)

# load config
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)
CHANNEL_IDS = config["discord"]["channels_tracked"]["ids"]
AUTHORISED_USER_IDS = config["discord"]["authorised_users"]["ids"]


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
bot = commands.Bot(command_prefix='/', intents=intents)

def main():
    @bot.command()
    @commands.check(check_auth)
    async def test(ctx):
        logging.info(f"Command triggered. Name:test, Author: {ctx.author.id}, Channel: {ctx.channel.id}")
        await ctx.send("Hello. This bot is working 👌")

    @bot.event
    async def on_ready():
        logging.info("Bot is ready ✅")
        logging.info("Syncing slash commands to command tree")
        await bot.tree.sync()

    bot.run(BOT_TOKEN)


if __name__ == "__main__":
    main()
