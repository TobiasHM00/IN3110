import datetime

import altair as alt
import numpy.testing as nt
import pytest
from strompris import (
    fetch_day_prices,
    fetch_prices,
    plot_activity_prices,
    plot_daily_prices,
    plot_prices,
)

location_codes = {f"NO{i}" for i in range(1, 6)}


def test_fetch_day_prices_defaults():
    df_default = fetch_day_prices()
    df_expected = fetch_day_prices(date=datetime.date.today(), location="NO1")
    assert (df_default.time_start == df_expected.time_start).all()
    assert (df_default.NOK_per_kWh == df_expected.NOK_per_kWh).all()


def test_fetch_day_prices_columns():
    df = fetch_day_prices()
    assert "time_start" in df.columns
    assert "NOK_per_kWh" in df.columns
    assert isinstance(df.NOK_per_kWh[0], float)
    assert isinstance(df.time_start[0], datetime.datetime)


@pytest.mark.parametrize(
    "date, location, expected_NOK_0, expected_NOK_end",
    [
        (datetime.date(2023, 10, 2), "NO1", 0.00068, 0.01677),
        (datetime.date(2023, 11, 6), "NO5", 0.57667, 0.86341),
    ],
)
def test_fetch_day_prices(date, location, expected_NOK_0, expected_NOK_end):
    df = fetch_day_prices(date=date, location=location)
    assert (df.time_start.dt.date == date).all()
    # sort by time, in case it's not already sorted
    df = df.sort_values("time_start")
    assert df.iloc[0].NOK_per_kWh == expected_NOK_0
    assert df.iloc[-1].NOK_per_kWh == expected_NOK_end


def test_fetch_prices_columns():
    df = fetch_prices(days=1, locations=["NO2"])
    assert "time_start" in df.columns
    assert "NOK_per_kWh" in df.columns
    assert "location_code" in df.columns
    assert isinstance(df.NOK_per_kWh[0], float)
    assert isinstance(df.time_start[0], datetime.datetime)
    assert set(df.location_code.unique()) == {"NO2"}


@pytest.mark.parametrize(
    "end, location, column, expected",
    [
        (
            "2023-11-01",
            "NO1",
            "1h change",
            -0.152,
        ),
        (
            "2023-11-02",
            "NO2",
            "24h change",
            -0.489,
        ),
        (
            "2023-11-08",
            "NO3",
            "7d change",
            0.390,
        ),
    ],
)
def test_fetch_prices_changes_in4110(
    end,
    location,
    column,
    expected,
):
    """
    Test task 5.4, only for in4110
    """
    end_date = datetime.datetime.strptime(end, "%Y-%m-%d").date()
    day_df = fetch_day_prices(end_date, location=location).sort_values("time_start")
    if column == "7d change":
        days = 8
    else:
        days = 2
    df = fetch_prices(end_date=end_date, days=days, locations=["NO1", "NO2", "NO3"])
    if column not in df.columns:
        pytest.skip(f"Missing '{column}' column in {df.columns}; Only for in4110")
    assert isinstance(df[column].iloc[-1], float)

    # get the first row for the last day
    # print(df, location, (df.location_code == location).sum())
    print(df.time_start.dt.day.unique())
    print(df[df.time_start.dt.date == end])
    df = df[df.location_code == location]
    first_day_values = df[df.time_start == day_df.time_start.min()][column]
    assert len(first_day_values) == 1
    first_day_value = first_day_values.iloc[0]
    nt.assert_almost_equal(first_day_value, expected, decimal=3)


def test_fetch_prices_default():
    df_default = fetch_prices()
    df_expected = fetch_prices(
        end_date=datetime.date.today(),
        days=7,
        locations=[f"NO{i}" for i in range(1, 6)],
    )
    assert len(df_default) == len(df_expected)
    assert set(df_default.location_code.unique()) == location_codes
    assert df_default.time_start.max() == df_expected.time_start.max()
    assert df_default.time_start.min() == df_expected.time_start.min()


def test_fetch_prices_one_day():
    date = datetime.date(2023, 11, 5)
    location = "NO1"
    df_day = fetch_day_prices(date)
    df = fetch_prices(end_date=date, days=1, locations=[location])
    assert "location" in df.columns
    assert "location_code" in df.columns
    assert (df["location"] == "Oslo").all()
    assert (df["location_code"] == "NO1").all()
    assert (df["time_start"] == df_day["time_start"]).all()


def test_plot_prices():
    # this test doesn't verify much of the output,
    # only that the function works without error
    df = fetch_prices(
        end_date=datetime.date(2023, 10, 30), days=3, locations=["NO1", "NO2"]
    )
    chart = plot_prices(df)
    assert isinstance(chart, alt.Chart)
    chart_dict = chart.to_dict()
    assert chart.mark == "line"
    # could assert encodings here


def test_plot_daily_prices():
    # this test doesn't verify the output,
    # only that the function works
    df = fetch_prices(
        end_date=datetime.date(2023, 10, 30), days=3, locations=["NO1", "NO2"]
    )
    try:
        chart = plot_daily_prices(df)
    except NotImplementedError:
        pytest.skip("5.4 (in4110 only): plot_daily_prices not implemented")
    if chart is None:
        pytest.skip("5.4 (in4110 only): plot_daily_prices not implemented")

    assert isinstance(chart, alt.Chart)
    chart_dict = chart.to_dict()
    # could assert something about encodings here,
    # but too much


# Task 5.6


@pytest.mark.parametrize(
    "activity, minutes, location",
    [
        ("shower", 10, "NO3"),
        ("baking", 30, "NO1"),
        ("heat", 5, "NO5"),
    ],
)
def test_plot_activity(activity, minutes, location):
    prices = fetch_prices(locations=[location], days=1)
    try:
        chart = plot_activity_prices(prices, activity=activity, minutes=minutes)
    except NotImplementedError as e:
        pytest.skip(str(e))

    assert isinstance(chart, alt.Chart)
    chart.to_dict()  # noqa
    # can't assert too much about the chart
