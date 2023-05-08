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
    @bot.tree.command(name="test", description="Check if EngagementBot is working")
    @app_commands.check(check_auth)
    async def test(interaction: discord.Interaction):
        logging.info(f"Command triggered. Name:test, Author: {interaction.user.id}, Channel: {interaction.channel.id}")
        await interaction.response.send_message("This bot is working 👌")

    @bot.tree.command(name="hst", description="Get engagement history for tracked channels (requires auth)")
    @app_commands.check(check_auth)
    @app_commands.describe(after_date="Get history after this date (YYYY-MM-DD)", freq="Engagement sampling frequency (e.g. D for daily)")
    async def hst(interaction: discord.Interaction, after_date: str = "2022-01-01", freq: str = "D"):
        logging.info(f"Command triggered. Name:hst, Author: {interaction.user.id}, Channel: {interaction.channel.id}")

        # defer response while calculating
        await interaction.response.defer()

        # get list of tracked channels
        logging.info(f"Collecting tracked channels")
        tracked_channels = []
        for channel_id in CHANNEL_IDS:
            tracked_channels.append(bot.get_channel(channel_id))
        logging.info(f"Found {len(tracked_channels)} channels")

        # get channel message history for tracked channels
        after_date_dt = datetime.strptime(after_date, "%Y-%m-%d")
        hist_list = []
        for ch in tracked_channels:
            logging.info(f"Getting message history for channel {ch.id} since {after_date}")
            msg_counter = 0
            async for message in ch.history(after=after_date_dt):
                msg_counter += 1
                historical_msg = HistoricalDiscordMessage(
                    date_time=message.created_at,
                    channel_id=ch.id,
                    author_id=message.author.id,
                    reactions=len(message.reactions)
                )
                hist_list.append(historical_msg)
            logging.info(f"Found a total of {msg_counter} messages for channel: {ch.id}")

        # transform message history to get summary
        logging.info(f"Resampling and summarising message history. Freq: {freq}")
        df = hist_msg_list_to_pandas_df(hist_list)
        summary_df = summarise_counts_by_group_and_freq(
            df=df, 
            groups=["channel_id", "author_id"], 
            freq=freq
        )
        out_df = summarise_counts(summary_df=summary_df)

        # return summary (send or attach)
        file_path = "./summary.csv"
        logging.info(f"Creating temporary file: {file_path}")
        out_df.reset_index().to_csv(file_path, index=False)
        logging.info(f"Replying with message count history and attached file: {file_path}")
        file = discord.File(file_path)

        embed = get_hist_summary_discord_embed(
            since=after_date, 
            freq=freq, 
            channel_names=tracked_channels, 
            embed_title="Historical Engagement"
        )
        embed.set_footer(text="Please find the summary attached.")

        # send interaction history
        await interaction.followup.send(embed=embed, file=file)

        # remove temp file
        try:
            os.remove(file_path)
            logging.info(f"Removed temporary file: {file_path}")
        except PermissionError:
            logging.warning(f"Failed to remove file due to permission error: {file_path}")

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
