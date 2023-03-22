import discord
import datetime
import pytz
from typing import List


class EngagementBot(discord.Client):
    def __init__(self, intents, channel_ids: List[str]):
        super().__init__(intents=intents)
        self.channel_ids = channel_ids
        self.engagement_summary = {}

    async def on_ready(self) -> dict:
        print(f"Logged on as {self.user}")

        # only consider messages from the last day
        since_time = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=1)

        for channel_id in self.channel_ids:
            channel = self.get_channel(channel_id)
            messages = await channel.history(
                limit=None,
                after=since_time
            ).flatten()

            # count the number of messages and reactions
            num_messages = len(messages)
            num_reactions = 0
            for message in messages:
                num_reactions += len(message.reactions)

            # update engagement results
            self.engagement_summary[channel.name] = {
                "num_messages": num_messages,
                num_reactions: num_reactions
            }

        print(f"\nEngagement Summary\n------------------\n\n{self.engagement_summary}\n")

        await self.close()
        return self.engagement_summary