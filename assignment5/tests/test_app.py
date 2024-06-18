import datetime
import re
from urllib.parse import urlencode, urljoin, urlparse

import altair as alt
import pandas as pd
import pytest
from bs4 import BeautifulSoup

location_codes = {f"NO{i}" for i in range(1, 6)}


def get_content_type(response):
    """Return the content-type of an HTTP response

    text/html or application.json

    (without trailing `; charset=utf-8`)
    """
    content_type = response.headers["Content-Type"]
    return content_type.split(";", 1)[0].strip()


def test_main_page(client):
    response = client.get("/")
    assert response.status_code == 200
    content_type = get_content_type(response)
    assert content_type == "text/html"
    # check for some expected elements
    page = BeautifulSoup(response.text, "html.parser")
    assert page.title.text == "Strømpris"


def test_form_input(client):
    response = client.get("/")
    assert response.status_code == 200
    content_type = get_content_type(response)
    assert content_type == "text/html"
    # check for some expected elements
    page = BeautifulSoup(response.text, "html.parser")
    form = page.find("form", id="price-form")
    assert form is not None
    # check end input
    end_input = form.find("input", attrs={"name": "end"})
    assert end_input, "Missing input for `name=end`"
    assert end_input["type"] == "date", "end date input should have type=date"
    # could check min, max but these aren't required

    # check days input
    days_input = form.find("input", attrs={"name": "days"})
    assert days_input, "Missing input for `name=days`"
    assert days_input["type"] == "number", "days input should have type=number"

    # check location inputs
    locations_inputs = form.find_all("input", attrs={"name": "locations"})
    assert locations_inputs

    location_values = []
    for location_input in locations_inputs:
        assert (
            location_input["type"] == "checkbox"
        ), "locations inputs should have type=checkbox"
        location_values.append(location_input.attrs.get("value"))

    assert sorted(location_values) == sorted(location_codes)


@pytest.mark.parametrize(
    "locations, end, days",
    [
        (None, None, None),
        [["NO1"], "2023-11-05", 2],
        [["NO1", "NO2"], "2023-11-03", 1],
    ],
)
def test_plot_prices_json(client, locations, end, days):
    params = {}
    if locations:
        params["locations"] = locations
    else:
        locations = sorted(location_codes)
    if end:
        params["end"] = end
    else:
        end = datetime.date.today().isoformat()
    if days:
        params["days"] = days
    else:
        days = 7

    end_date = datetime.date.fromisoformat(end)

    url = "/plot_prices.json?" + urlencode(params, doseq=True)
    print(f"Fetching {url}")

    response = client.get(url)
    assert response.status_code == 200
    content_type = get_content_type(response)
    assert content_type == "application/json"
    chart_data = response.json()
    # validate chart
    chart = alt.Chart.from_dict(chart_data)
    # load datasets
    dataframes = [
        pd.DataFrame.from_dict(data) for data in chart_data["datasets"].values()
    ]
    for df in dataframes:
        assert "time_start" in df.columns
        assert "location" in df.columns
        assert "location_code" in df.columns

        assert set(df.location_code.unique()) == set(locations)
        time_start = pd.to_datetime(df.time_start)
        assert time_start.max().date() == end_date
        assert time_start.min().date() == end_date - datetime.timedelta(days=days - 1)


def test_nav_links(client):
    response = client.get("/")
    # check for some expected elements
    page = BeautifulSoup(response.text, "html.parser")
    doc_link = page.find("a", href=re.compile("/docs/?"))
    assert doc_link, "Found no link to fastapi docs: `<a href=/docs"

    help_link = page.find("a", href=re.compile("/help/?"))
    assert help_link, "Found no link to fastapi docs: `<a href=/help"


def test_fastapi_docs(client):
    response = client.get("/docs")
    assert response.status_code == 200
    content_type = get_content_type(response)
    assert content_type == "text/html"
    page = BeautifulSoup(response.text, "html.parser")
    assert "FastAPI" in page.title.get_text()

    response = client.get("/openapi.json")
    assert response.status_code == 200
    content_type = get_content_type(response)
    assert content_type == "application/json"
    spec = response.json()
    assert "paths" in spec
    paths = spec["paths"]
    assert "/plot_prices.json" in paths


@pytest.fixture
def doc_pages(client):
    doc_root = "/help/"
    response = client.get(doc_root)
    assert response.status_code == 200
    content_type = get_content_type(response)
    assert content_type == "text/html"
    # collect all the pages
    pages = {}
    # check for some expected elements
    pages[doc_root] = page = BeautifulSoup(response.text, "html.parser")
    urls = set()
    for link in page.find_all("a"):
        url = link.get("href", "#")
        # ignore internal anchors
        if not url or url.startswith("#"):
            continue
        url = urljoin(doc_root, url)
        if (
            url == doc_root
            or not url.startswith(doc_root)
            or url.startswith(doc_root + "_sources/")
        ):
            continue
        # include only the path
        urls.add(urlparse(url).path)
    for url in urls:
        r = client.get(url)
        if r.status_code != 200:
            pages[url] = r.status_code
            continue
        content_type = get_content_type(r)
        if content_type != "text/html":
            # ignore non-html files
            continue
        pages[url] = BeautifulSoup(r.text, "html.parser")
    return pages


@pytest.mark.parametrize(
    "expected",
    [
        "fetch_day_prices",
        "fetch_prices",
        "plot_prices",
        # "plot_daily_prices",
        # "plot_activity_prices",
    ],
)
def test_sphinx_docs(client, doc_pages, expected):
    found = False
    checked = []
    for path, page in doc_pages.items():
        if isinstance(page, int):
            continue
        checked.append(path)
        page_text = page.get_text()
        if expected in page_text:
            found = path
            print(f"Found {expected} in {path}")
            break
    assert found, f"Never found docs for {expected} in {', '.join(checked)}"


# Task 5.6


def test_plot_activity_html(client):
    r = client.get("/activity")
    assert r.status_code == 200
    content = r.text
    # can't assert too much about structure,
    # but check that plot_activity.json shows up somewhere
    assert "plot_activity.json" in content
    # and that the activity choices show up somewhere
    for activity in ("shower", "baking", "heat"):
        assert activity in content.lower()


@pytest.mark.parametrize(
    "activity, minutes, location",
    [
        ("shower", 10, "NO1"),
        ("baking", 30, "NO2"),
        ("heat", 5, "NO4"),
    ],
)
def test_plot_activity_json(client, activity, minutes, location):
    params = {
        "activity": activity,
        "minutes": minutes,
        "location": location,
    }
    r = client.get("/plot_activity.json", params=params)
    assert r.status_code == 200
    content_type = get_content_type(r)
    assert content_type == "application/json"
    chart = alt.Chart.from_dict(r.json())
    # can't assert too much about the chart
