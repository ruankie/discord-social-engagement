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

    Args:
        hist_list (List[HistoricalDiscordMessage]): A list of historical discord messages.
    
    Returns:
        pd.DataFrame: A dataframe of the message list.
    """
    dict_list = [msg.to_dict() for msg in hist_list]
    df = pd.DataFrame(data=dict_list)
    df["date_time"] = pd.to_datetime(df["date_time"])
    df = df.set_index("date_time")
    return df

def summarise_counts_by_group_and_freq(df: pd.DataFrame, groups: List[str] = ["channel_id", "author_id"], freq: str = "D") -> pd.DataFrame:
    """
    Take a pandas DataFrame of historical discord messages,
    group them by the given columns and resample them to
    a given frequency. This produces a summary count of
    messages and reactions per group by time freq.

    Args:
        df (pd.DataFrame): A pandas DataFrame of historical discord messages.
        groups (List[str]): A list of column names to group by.
        freq (str): A resample frequency that pandas will use to resample data.

    Returns:
        pd.DataFrame: A summary count of messages and reactions per group by time freq.
    """
    summary_df = df.groupby(by=groups, as_index=True)\
        .resample(rule=freq)\
        .agg(
            messages=("reactions","count"), 
            reactions=("reactions","sum")
            )\
        .reset_index()
    
    return summary_df

def summarise_counts(summary_df: pd.DataFrame) -> pd.DataFrame:
    """
    Take a pandas DataFrame that has been summarised by
    group and time freq and give a more succinct summary
    of counts for reactions, messages, and unique_authors.

    Args:
        summary_df (pd.DataFrame): a pandas DataFrame that has been summarised by group and time freq.

    Returns:
        pd.DataFrame: A summary of counts for reactions, messages, and unique_authors.
    """
    out_df = summary_df.groupby(by="date_time", as_index=True)[["reactions", "messages"]].sum()
    out_df["unique_authors"] = summary_df.groupby(by="date_time", as_index=True)["author_id"].nunique()
    out_df
    
    return summary_df