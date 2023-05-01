# based on https://www.linkedin.com/pulse/discord-bot-part-2-slash-commands-leandro-fumio-kino
# check this out next: https://www.youtube.com/watch?v=jh1CtQW4DTo

import os
import discord
from discord.ext import commands
from discord import app_commands
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


def check_auth(interaction: discord.Interaction) -> bool:
    """
    Check if the command was triggered by an authorised user.
    """
    return interaction.user.id in AUTHORISED_USER_IDS

# load env vars
logging.info("Loading env vars")
load_dotenv()
BOT_TOKEN = os.environ["BOT_TOKEN"]

# define intents
logging.info("Defining intents")
intents = discord.Intents.default()
intents.message_content = True

logging.info("Setting up discord bot")
bot = commands.Bot(command_prefix='!', intents=intents)

def main():
    @bot.tree.command(name="test")
    @app_commands.check(check_auth)
    async def test(interaction: discord.Interaction):
        logging.info(f"Command triggered. Name:test, Author: {interaction.user.id}, Channel: {interaction.channel.id}")
        await interaction.response.send_message("Hello. This bot is working 👌")

    @bot.tree.command(name="say")
    @app_commands.check(check_auth)
    @app_commands.describe(thing_to_say="What the bot must say", another_thing="Another thing")
    async def say(interaction: discord.Interaction, thing_to_say: str, another_thing: str):
        logging.info(f"Command triggered. Name:say, Author: {interaction.user.id}, Channel: {interaction.channel.id}")
        await interaction.response.send_message(f"{thing_to_say}, {another_thing}")

    @bot.tree.command(name="sync")
    @app_commands.check(check_auth)
    async def sync(interaction: discord.Interaction):
        logging.info(f"Command triggered. Name:sync, Author: {interaction.user.id}, Channel: {interaction.channel.id}")
        logging.info("Syncing slash commands to command tree")
        try:
            synced = await bot.tree.sync()
            msg = f"Synced {len(synced)} commands"
            logging.info(msg)
            await interaction.response.send_message(msg)
        except Exception as ex:
            msg = "Could not sync commands to bot tree"
            logging.error(msg)
            await interaction.response.send_message(msg)

    @bot.event
    async def on_ready():
        logging.info("Bot is ready ✅")
        logging.info("Syncing slash commands to command tree")
        try:
            synced = await bot.tree.sync()
            logging.info(f"Synced {len(synced)} commands")
        except Exception as ex:
            logging.error("Could not sync commands to bot tree")

    bot.run(BOT_TOKEN)


if __name__ == "__main__":
    main()
