"""
Task 4

collecting olympic statistics from wikipedia
"""

from __future__ import annotations
import os
from pathlib import Path
from bs4 import BeautifulSoup
import pandas as pd
from requesting_urls import get_html

import matplotlib.pyplot as plt

# Countries to submit statistics for
scandinavian_countries = ["Norway", "Sweden", "Denmark"]

# Summer sports to submit statistics for
summer_sports = ["Sailing", "Athletics", "Handball", "Football", "Cycling", "Archery"]


def report_scandi_stats(url: str, sports_list: list[str], work_dir: str | Path) -> None:
    """
    Given the url, extract and display following statistics for the Scandinavian countries:

      -  Total number of gold medals for for summer and winter Olympics
      -  Total number of gold, silver and bronze medals in the selected summer sports from sport_list
      -  The best country in number of gold medals in each of the selected summer sports from sport_list

    Display the first two as bar charts, and the last as an md. table and save in a separate directory.

    Parameters:
        url (str) : url to the 'All-time Olympic Games medal table' wiki page
        sports_list (list[str]) : list of summer Olympic games sports to display statistics for
        work_dir (str | Path) : (absolute) path to your current working directory

    Returns:
        None
    """

    # Make a call to get_scandi_stats
    # Plot the summer/winter gold medal stats
    # Iterate through each sport and make a call to get_sport_stats
    # Plot the sport specific stats
    # Make a call to find_best_country_in_sport for each sport
    # Create and save the md table of best in each sport stats

    work_dir = Path(work_dir)
    country_dict = get_scandi_stats(url)

    stats_dir = work_dir / "olympic_games_results"
    os.mkdir(stats_dir)
    plot_scandi_stats(country_dict, stats_dir)

    best_in_sport = []
    # Valid values for medal ["Gold" | "Silver" |"Bronze"]
    medal = "Gold"

    for sport in sports_list:
        results: dict[str, dict[str, int]] = {}
        for country, info in country_dict.items():
            results.update({country: get_sport_stats(info["url"], sport)})
        
        plot_sport_stats(results, sport, stats_dir)
        best_in_sport.append([sport, find_best_country_in_sport(results, medal)])
        
    headers = ["Sport", f"Best country in sport by {medal} medal"]
    df = pd.DataFrame(best_in_sport, columns=headers)
    table = df.to_markdown(index=False)

    # Save the output
    output_file = stats_dir / f"best_of_sport_by_{medal}.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(table)


def plot_sport_stats(
    results: dict[str, dict[str, int]],
    sport: str,
    stats_dir: str | Path
) -> None:
    """Plot the number of medals in the summer Olympix sport for each of the scandi countries as bars.

    Args:
        results (dict[str, dict[str, int]]): a nested dictionary of country country and the corresponding number of medals for each sport
        sport (str): name of summer Olympic sport in intrest. Should be used to plot a image for each sport
        stats_dir (str | Path): parent file path to save the plot in
    
    Returns:
        None
    """
    countries = []
    gold_medals = []
    silver_medals = []
    bronze_medals = []
    
    for country, info in results.items():
        countries.append(country)
        gold_medals.append(info["Gold"])
        silver_medals.append(info["Silver"])
        bronze_medals.append(info["Bronze"])        
    
    bar_width = 0.20
    x = range(len(countries))
    plt.figure(figsize=(10, 8))
    
    gold_bars = plt.bar(x, gold_medals, width=bar_width, color="red", label="Gold")
    silver_bars = plt.bar([i + bar_width for i in x], silver_medals, width=bar_width, color="blue", label="Silver")
    bronze_bars = plt.bar([i + bar_width*2 for i in x], bronze_medals, width=bar_width, color="purple", label="Bronze")

    plt.xticks([i + bar_width / 2 for i in x], countries, rotation=45, ha="right")    
    plt.xlabel("Countries")
    plt.ylabel(f"Number of medals in {sport}")
    plt.ylim((0,50))
    plt.title(f"Number of medals in {sport} for scandinavian countries in summer Olympic Games")
    plt.legend(loc="upper right")
    
    for gold, silver, bronze in zip(gold_bars, silver_bars, bronze_bars):
        plt.text(gold.get_x() + gold.get_width() / 2, gold.get_height(), gold.get_height(), ha='center', va='bottom')
        plt.text(silver.get_x() + silver.get_width() / 2, silver.get_height(), silver.get_height(), ha='center', va='bottom')
        plt.text(bronze.get_x() + bronze.get_width() / 2, bronze.get_height(), bronze.get_height(), ha='center', va='bottom')
    
    plt.savefig(stats_dir / f"{sport}_medal_ranking.png")
    

def get_scandi_stats(
    url: str,
) -> dict[str, dict[str, str | dict[str, int]]]:
    """Given the url, extract the urls for the Scandinavian countries,
       as well as number of gold medals acquired in summer and winter Olympic games
       from 'List of NOCs with medals' table.

    Parameters:
      url (str): url to the 'All-time Olympic Games medal table' wiki page

    Returns:
      country_dict: dictionary of the form:
        {
            "country": {
                "url": "https://...",
                "medals": {
                    "Summer": 0,
                    "Winter": 0,
                },
            },
        }

        with the tree keys "Norway", "Denmark", "Sweden".
    """

    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'class':'wikitable sortable'})
    base_url = "https://en.wikipedia.org"

    rows = table.find_all('tr')[1:]

    country_dict: dict[str, dict[str, str | dict[str, int]]] = {}

    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 0:    
            country_name = cols[0].text.strip().split()[0]

            if country_name in scandinavian_countries:
                summer_gold = int(cols[2].get_text())
                winter_gold = int(cols[7].get_text())

                country_url = base_url + f'/wiki/{country_name}_at_the_Olympics'
                country_dict[country_name] = {
                    "url": country_url,
                    "medals": {
                        "Summer": summer_gold,
                        "Winter": winter_gold,
                    },
                }

    return country_dict


def get_sport_stats(country_url: str, sport: str) -> dict[str, int]:
    """Given the url to country specific performance page, get the number of gold, silver, and bronze medals
      the given country has acquired in the requested sport in summer Olympic games.

    Parameters:
        - country_url (str) : url to the country specific Olympic performance wiki page
        - sport (str) : name of the summer Olympic sport in interest. Should be used to filter rows in the table.

    Returns:
        - medals (dict[str, int]) : dictionary of number of medal acquired in the given sport by the country
                          Format:
                          {"Gold" : x, "Silver" : y, "Bronze" : z}
    """
    html = get_html(country_url)
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'class': 'wikitable sortable plainrowheaders jquery-tablesorter'})

    medals = {
        "Gold": 0,
        "Silver": 0,
        "Bronze": 0,
    }

    rows = table.find_all('tr')

    for row in rows:
        tableSport = row.find('th')
        sportText = tableSport.get_text().strip()
        
        if sportText == sport:
            tableMedals = row.find_all('td')
            medals["Gold"] = int(tableMedals[0].get_text())
            medals["Silver"] = int(tableMedals[1].get_text())
            medals["Bronze"] = int(tableMedals[2].get_text())
        
    return medals


def find_best_country_in_sport(
    results: dict[str, dict[str, int]], medal: str = "Gold"
) -> str:
    """Given a dictionary with medal stats in a given sport for the Scandinavian countries, return the country
        that has received the most of the given `medal`.

    Parameters:
        - results (dict) : a dictionary of country specific medal results in a given sport. The format is:
                        {"Norway" : {"Gold" : 1, "Silver" : 2, "Bronze" : 3},
                         "Sweden" : {"Gold" : 1, ....},
                         "Denmark" : ...
                        }
        - medal (str) : medal type to compare for. Valid parameters: ["Gold" | "Silver" |"Bronze"]. Should be used as a key
                          to the medal dictionary.
    Returns:
        - best (str) : name of the country(ies) leading in number of gold medals in the given sport
                       If one country leads only, return its name, like for instance 'Norway'
                       If two countries lead return their country separated with '/' like 'Norway/Sweden'
                       If all or none of the countries lead, return string 'None'
    """
    valid_medals = {"Gold", "Silver", "Bronze"}
    if medal not in valid_medals:
        raise ValueError(
            f"{medal} is invalid parameter for ranking, must be in {valid_medals}"
        )

    # Get the requested medals and determine the best
    best = ""

    norway = results["Norway"][medal]
    sweden = results["Sweden"][medal]
    denmark = results["Denmark"][medal]
    if norway > sweden and norway > denmark:
        best = "Norway"
    elif sweden > norway and sweden > denmark:
        best = "Sweden"
    elif denmark > norway and denmark > sweden:
        best = "Denmark"
    elif norway == sweden and norway > denmark:
        best = "Norway/Sweden"
    elif norway == denmark and norway > sweden:
        best = "Norway/Denmark"
    elif sweden == denmark and sweden > norway:
        best = "Sweden/Denmark"
    else:
        return "None"
    
    return best


# Define your own plotting functions and optional helper functions


def plot_scandi_stats(
    country_dict: dict[str, dict[str, str | dict[str, int]]],
    output_parent: str | Path | None = None,
) -> None:
    """Plot the number of gold medals in summer and winter games for each of the scandi countries as bars.

    Parameters:
      results (dict[str, dict[str, int]]) : a nested dictionary of country country and the corresponding number of summer and winter
                            gold medals from 'List of NOCs with medals' table.
                            Format:
                            {"country_name": {"Summer" : x, "Winter" : y}}
      output_parent (str | Path) : parent file path to save the plot in
    Returns:
      None
    """
    countries = []
    summer_medals = []
    winter_medals = []
    
    for country, info in country_dict.items():
        countries.append(country)
        medals = info["medals"]
        summer_medals.append(medals["Summer"])
        winter_medals.append(medals["Winter"])
    
    bar_width = 0.20
    x = range(len(countries))
    plt.figure(figsize=(10, 6))
    
    summer_bar = plt.bar(x, summer_medals, width=bar_width, color="red", label="Summer")
    winter_bars = plt.bar([i + bar_width for i in x], winter_medals, width=bar_width, color="blue", label="Winter")

    plt.xticks([i + bar_width / 2 for i in x], countries, rotation=45, ha="right")    
    plt.xlabel("Countries")
    plt.ylabel("Number of gold medals")
    plt.ylim((0,200))
    plt.title("Number of gold medals for scandinavian countries in Olympic Games")
    plt.legend(loc="upper right")
    
    for summer, winter in zip(summer_bar, winter_bars):
        plt.text(summer.get_x() + summer.get_width() / 2, summer.get_height(), summer.get_height(), ha='center', va='bottom')
        plt.text(winter.get_x() + winter.get_width() / 2, winter.get_height(), winter.get_height(), ha='center', va='bottom')
    
    plt.savefig(output_parent / "total_medal_ranking.png")


# run the whole thing if called as a script, for quick testing
if __name__ == "__main__":
    url = "https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table"
    work_dir = "C:/Users/tobbe/OneDrive/Dokumenter/Skole/H2023/IN3110/IN3110-tobiashm/assignment4"    
    report_scandi_stats(url, summer_sports, work_dir)
