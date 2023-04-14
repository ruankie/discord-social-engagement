import os
import yaml
import discord
from dotenv import load_dotenv
from bot import EngagementBot


def main():
    # load config
    with open("./bot_config.yml", "r") as f:
        yaml_content = f.read()
        config = yaml.safe_load(yaml_content)

    # load env vars
    load_dotenv()
    BOT_TOKEN = os.environ["BOT_TOKEN"]
    CHANNEL_IDS = config["discord"]["channel_ids"]

    # define intents
    intents = discord.Intents.default()
    intents.members = True

    # create and run bot
    bot = EngagementBot(intents=intents, channel_ids=CHANNEL_IDS)
    engagement_summary = bot.run(BOT_TOKEN)


if __name__ == "__main__":
    main()
