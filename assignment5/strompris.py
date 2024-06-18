#!/usr/bin/env python3
"""
Fetch data from https://www.hvakosterstrommen.no/strompris-api
and visualize it.

Assignment 5
"""
from __future__ import annotations

import datetime
import warnings

import altair as alt
import pandas as pd
import requests
import requests_cache

# install an HTTP request cache
# to avoid unnecessary repeat requests for the same data
# this will create the file http_cache.sqlite
requests_cache.install_cache()

# suppress a warning with altair 4 and latest pandas
warnings.filterwarnings("ignore", ".*convert_dtype.*", FutureWarning)


# task 5.1:


def fetch_day_prices(date: datetime.date = None, location: str = "NO1") -> pd.DataFrame:
    """Fetch one day of data for one location from hvakosterstrommen.no API

    Args:
        date (datetime.date, optional): Date of day I want API respons from. Defaults to None.
        location (str, optional): String with location. Defaults to "NO1".

    Returns:
        pd.DataFrame: DataFrame for one singel day
    """
    if date is None:
        date = datetime.date.today()

    date_str = date.strftime("%Y/%m-%d")
    url = f"https://www.hvakosterstrommen.no/api/v1/prices/{date_str}_{location}.json"
    r = requests.get(url)
    if r.status_code != 200:
        print("Error!! " + r.status_code)
        exit(-1)
    
    data = pd.DataFrame.from_dict(r.json())
    data["time_start"] = pd.to_datetime(data["time_start"], utc=True).dt.tz_convert("Europe/Oslo")
    return data[["NOK_per_kWh", "time_start"]]


# LOCATION_CODES maps codes ("NO1") to names ("Oslo")
LOCATION_CODES = {
    "NO1":"Oslo",
    "NO2":"Kristiansand",
    "NO3":"Trondheim",
    "NO4":"Tromsø",
    "NO5":"Bergen", 
    }

# task 1:


def fetch_prices(
    end_date: datetime.date = None,
    days: int = 7,
    locations: list[str] = tuple(LOCATION_CODES.keys()),
) -> pd.DataFrame:
    """Fetch prices for multiple days and locations into a single DataFrame

    Args:
        end_date (datetime.date, optional): date for last day information should be gather from. Defaults to None.
        days (int, optional): int with number of days. Defaults to 7.
        locations (list[str], optional): list with strings of locations. Defaults to tuple(LOCATION_CODES.keys()).

    Returns:
        pd.DataFrame: Full DataFrame with days day
    """
    if end_date is None:
        end_date = datetime.date.today()

    start_date = end_date - datetime.timedelta(days=days-1)
    
    days_list = []
    for day in range(days):
        days_list.append(start_date+datetime.timedelta(day))
    
    result_df = pd.DataFrame()
    for single_date in days_list:
        for location in locations:
            day_data = fetch_day_prices(single_date, location)
            day_data["location_code"] = location
            day_data["location"] = LOCATION_CODES[location]
            result_df = pd.concat([result_df, day_data], ignore_index=True)

    return result_df


# task 5.1:


def plot_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot energy prices over time

    x-axis should be time_start
    y-axis should be price in NOK
    each location should get its own line

    Args:
        df (pd.DataFrame): Complete DataFram with info about energyprices from each location

    Returns:
        alt.Chart: A altair chart
    """
    chart = (
        alt.Chart(df)
        .mark_line()
        .encode(x = 'time_start:T', y = 'NOK_per_kWh:Q', color = 'location:N')
        .properties(title = 'Energy Prices Over Time', width = 800, height = 400)
    )
    return chart

# Task 5.4


def plot_daily_prices(df: pd.DataFrame) -> alt.Chart:
    """Plot the daily average price

    x-axis should be time_start (day resolution)
    y-axis should be price in NOK

    You may use any mark.

    Make sure to document arguments and return value...
    """
    raise NotImplementedError("Remove me when you implement this task (in4110 only)")
    ...


# Task 5.6

ACTIVITIES = {
    # activity name: energy cost in kW
    ...
}


def plot_activity_prices(
    df: pd.DataFrame, activity: str = "shower", minutes: float = 10
) -> alt.Chart:
    """
    Plot price for one activity by name,
    given a data frame of prices, and its duration in minutes.

    Make sure to document arguments and return value...
    """
    raise NotImplementedError("Remove me when you implement this optional task")

    ...


def main():
    """Allow running this module as a script for testing."""
    df = fetch_prices()
    chart = plot_prices(df)
    # showing the chart without requiring jupyter notebook or vs code for example
    # requires altair viewer: `pip install altair_viewer`
    chart.show()


if __name__ == "__main__":
    main()
