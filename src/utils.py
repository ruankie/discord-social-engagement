import pandas as pd
from datetime import datetime, timedelta
from typing import List, Union
from dataclasses import dataclass



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



def hist_list_to_pandas_df(hist_list: List[HistoricalDiscordMessage]) -> pd.DataFrame:
    """
    Take a list of HistoricalDiscordMessages and convert it into a
    pandas DataFrame for further processing
    """
    pass