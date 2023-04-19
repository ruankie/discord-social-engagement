import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import yaml
from src.utils import (
    HistoricalDiscordMessage, 
    hist_msg_list_to_pandas_df, 
    summarise_counts_by_group_and_freq, 
    summarise_counts
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
FREQ = config["general"]["resample_freq"]


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
    @commands.check(check_auth)
    async def test(ctx):
        logging.info(f"Command triggered. Name:test, Author: {ctx.author.id}, Channel: {ctx.channel.id}")
        await ctx.send("Hello. This bot is working 👌")

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

    @bot.command()
    @commands.check(check_auth)
    async def hst(ctx):
        logging.info(f"Command triggered. Name:hst, Author: {ctx.author.id}, Channel: {ctx.channel.id}")

        # get list of tracked channels
        logging.info(f"Collecting tracked channels")
        tracked_channels = []
        for channel_id in CHANNEL_IDS:
            tracked_channels.append(bot.get_channel(channel_id))
        logging.info(f"Found {len(tracked_channels)} channels")

        # get channel message history for tracked channels
        hist_list = []
        for ch in tracked_channels:
            logging.info(f"Getting message history for channel: {ch.id}")
            msg_counter = 0
            async for message in ch.history(limit=2000):
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
        logging.info("Transforming and summarising message history")
        df = hist_msg_list_to_pandas_df(hist_list)
        summary_df = summarise_counts_by_group_and_freq(
            df=df, 
            groups=["channel_id", "author_id"], 
            freq=FREQ
        )
        out_df = summarise_counts(summary_df=summary_df)

        # return summary (send or attach)
        file_path = "./summary.csv"
        logging.info(f"Creating temporary file: {file_path}")
        out_df.reset_index().to_csv(file_path, index=False)
        logging.info(f"Replying with message count history and attached file: {file_path}")
        file = discord.File(file_path)
        await ctx.send(file=file, content=f"Here is your message count history:")
        os.remove(file_path)
        logging.info(f"Removed temporary file: {file_path}")

    bot.run(BOT_TOKEN)


if __name__ == "__main__":
    main()
