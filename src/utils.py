import pandas as pd
from datetime import datetime, timedelta
from typing import List, Union
from dataclasses import dataclass, asdict


@dataclass
class HistoricalDiscordMessage:
    """
    Holds information on messages gathered from discord history.

    Args:
        date_time (Union[datetime, str]): The date and time the message was sent.
        channel_id (int): The discord channel id that the message is from.
        author_id (int): The message author's user id on discord.
        reactions (int): The number of reactions the message received.
    """
    date_time: Union[datetime, str]
    channel_id: int
    author_id: int
    reactions: int

    def to_dict(self):
        """
        Returns a dictionary representation of the object and its attributes.
        """
        return asdict(self)


def hist_msg_list_to_pandas_df(hist_list: List[HistoricalDiscordMessage]) -> pd.DataFrame:
    """
    Take a list of HistoricalDiscordMessages and convert it into a
    pandas DataFrame for further processing.
    """
    dict_list = [msg.to_dict for msg in hist_list]
    df = pd.DataFrame(data=dict_list)
    df["date_time"] = pd.to_datetime(df["date_time"])
    df = df.set_index("date_time")
    return df