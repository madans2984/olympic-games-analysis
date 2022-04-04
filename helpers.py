"""
Functions for scraping and cleaning olympics data.
"""

# Disable pylint's E1101: Instance of 'TextFileReader' has no '___' member
# (no-member) error, because it's a problem inside of the pandas library
# pylint: disable=E1101

# Disable pylint's E1136: Value '___' is unsubscriptable
# (unsubscriptable-object), because it's a problem inside of the pandas library
# pylint: disable=E1136

# Disable pylint's E1137: '___' does not support item assignment
# (unsupported-assignment-operation), because it's a problem inside of the
# pandas library
# pylint: disable=E1137

import re # regex library for removing text in square brackets
import pandas as pd  # library for data analysis
import requests  # library to handle requests
from bs4 import BeautifulSoup  # library to parse HTML documents
# import grama as gr  # library for data cleaning


def table_scrape(url, index=0):
    """
    Scrapes a single table from a wikipedia page using the url and the index of
    the table on the page that should be scraped (defaults to index 0, the
    first table).

    Args:
        url: string representing the url of a wikipedia article.
        index: index of the table on the wikipedia page (optional).
    Returns:
        A pandas dataframe consisting of the data in the wikitable.
    """
    response = requests.get(url)
    # Status code must be 200 to legally scrape
    if response.status_code == 200:
        # Parse data from the html into a beautifulsoup object
        soup = BeautifulSoup(response.text, "html.parser")
        tables = soup.findAll("table", {"class": "wikitable"})
        data_frame = pd.read_html(str(tables[index]))
        # Convert list to dataframe
        data_frame = pd.DataFrame(data_frame[0])
        return data_frame
    print("Error: This table should not be scraped due to its status"
              " code.")
    return None


def scrape_medal_table(url, year, host):
    """
    Convert the medal table on the wikipedia page for an olympic games to a
    pandas dataframe.

    Makes each column (other than "Country") preface with the year of the games.

    Args:
        url: a string representing the wikipedia page for the olympics games to
            scrape
        year: an int or string representing the year of the olympic games page
            to be scraped so that the athlete count column can be properly named
        host: a string representing the host nation for that year, so that the
            "*" next to the host country's name can be deleted
    Returns:
        A pandas dataframe containing the scraped medal table.
    """
    table = table_scrape(url)
    # Rename columns to have the year in the title
    table.rename(columns={"NOC": "Country", "Nation": "Country",
                          "Gold": f"Gold-{year}", "Silver": f"Silver-{year}",
                          "Bronze": f"Bronze-{year}", "Total": f"Total-{year}"}, inplace=True)
    # Drop rank column because it's not relevant for our question
    table.drop(["Rank"], axis=1, inplace=True)
    table.replace({f"{host}*": f"{host}"}, inplace=True)

    # Remove final row containing total number of countries
    table = table[:-1]
    return table


def scrape_medal_data(output_path=None):
    """
    Scrapes medal data for desired years from Wikipedia and merges them into
    one dataframe.

    Args:
        output_path: name of file that the dataframe will save to (optional).
    Returns:
        The merged dataframe.
    """
    # Wikipedia pages to scrape
    pg_2004 = "https://en.m.wikipedia.org/wiki/2004_Summer_Olympics_medal_table"
    pg_2008 = "https://en.m.wikipedia.org/wiki/2008_Summer_Olympics_medal_table"
    pg_2012 = "https://en.m.wikipedia.org/wiki/2012_Summer_Olympics_medal_table"
    pg_2016 = "https://en.wikipedia.org/wiki/2016_Summer_Olympics_medal_table"

    # Scrape each page to a pandas dataframe, format with date, and remove "*"
    # next to each host country's name.
    medals_2004 = scrape_medal_table(pg_2004, "2004", "Greece")
    medals_2008 = scrape_medal_table(pg_2008, "2008", "China")
    medals_2012 = scrape_medal_table(pg_2012, "2012", "Great Britain")
    medals_2016 = scrape_medal_table(pg_2016, "2016", "Brazil")

    # Merge the 4 dataframes into 1, only keeping countries that medalled in
    # all 4 years
    medals_all = merge_dataframes([medals_2004, medals_2008, medals_2012, medals_2016],
                                  method="inner")

    # If a location to save a csv is given, save it there
    if output_path is not None:
        medals_all.to_csv(output_path, index=False)
    # Always return the dataframe
    return medals_all


def scrape_population_data(output_path=None):
    """
    Scrape population data from wikipedia.

    Args:
        output_path: name of file that the dataframe will save to (optional).
    Returns:
        Dataframe containing scraped population data.
    """
    # Scrape the second table on the wikipedia page for country populations
    wikipedia_page = ("https://en.wikipedia.org/wiki/List_of_countries_by_past_"
                      "and_projected_future_population#Estimates_between_the_years_1985_and_2015_"
                      "(in_thousands)")
    population = table_scrape(wikipedia_page, 1)

    # If a location to save a csv is given, save it there
    if output_path is not None:
        population.to_csv(output_path, index=False)
    # Always return the dataframe
    return population


def clean_population_data(input_path, output_path=None):
    """
    Clean population data from wikipedia by removing unnecessary years and
    percentages of population to leave whole numbers.

    The closest years' population was used for each year of the Olympics (i.e.
    population data in 2005 was used for the Olympic Games in 2004, population
    data in 2010 was used for the Games in both 2008 and 2010, and population
    data in 2015 was used for 2016. Population columns were renamed to
    correspond with Olympic Games' years. Special cases: renamed Great Britain
    as United Kingdom and Chinese Taipei as Taiwan.

    Args:
        input_path: a string representing the filepath of of the CSV of the
            dataframe that needs to be cleaned.
        output_path: name of file that the dataframe will save to (optional).
    Returns:
        The cleaned population dataframe.
    """
    population = pd.read_csv(input_path)
    # Drop unnecessary years
    population.drop(["1985", "1990", "1995", "2000", "%", "%.1", "%.2", "%.3", "%.4", "%.5", "%.6"],
                    axis=1, inplace=True)

    # Rename columns to be associated with the correct olympic years
    population.rename(columns={"Country (or dependent territory)": "Country",
                               "2005": "Pop-2004",
                               "2010": "Pop-2008",
                               "2015": "Pop-2016"}, inplace=True)
    # Create a column for the population in 2012 and duplicate 2008 into it
    population["Pop-2012"] = population["Pop-2008"]
    # Reorder population dataframe to be chronological
    population = population[["Country", "Pop-2004", "Pop-2008", "Pop-2012",
                             "Pop-2016"]]

    # Multiply each value by 1000 because wikipedia page has population in
    # thousands
    pop_columns = ["Pop-2004", "Pop-2008", "Pop-2012", "Pop-2016"]
    for col in pop_columns:
        population[col] = population[col]*1000

    # Rename the UK and Taiwan rows to match their olympic committee names
    population.replace({"United Kingdom": "Great Britain"}, inplace=True)
    population.replace({"Taiwan": "Chinese Taipei"}, inplace=True)

    # If a location to save a csv is given, save it there
    if output_path is not None:
        population.to_csv(output_path, index=False)
    # Always return the dataframe
    return population


def scrape_gdp_data(output_path=None):
    """
    Scrape the IMF's GDP per capita data from wikipedia.

    Args:
        output_path: name of file that the dataframe will save to (optional).
    Returns:
        A dataframe containing the scraped GDP data.
    """
    # Scrape the 3rd and 4th tables on the GDP (PPP) per capita wikipedia page
    wikipedia_page = ("https://en.wikipedia.org/wiki/"
                      "List_of_countries_by_past_and_projected_GDP_(PPP)_per_capita")
    gdp_2000s = table_scrape(wikipedia_page, 2)
    gdp_2010s = table_scrape(wikipedia_page, 3)

    # Merge the dataframes
    gdp_total = merge_dataframes([gdp_2000s, gdp_2010s],
                                 merge_on="Country (or dependent territory)")

    # If a location to save a csv is given, save it there
    if output_path is not None:
        gdp_total.to_csv(output_path, index=False)
    # Always return the dataframe
    return gdp_total


def clean_gdp_data(input_path, output_path=None):
    """
    Clean GDP data by dropping unnecessary years, renaming columns, and adding
    missing competitors.

    Special cases: renamed Great Britain as United Kingdom and Chinese Taipei
    as Taiwan; use the UN's GDP per capita for Cuba and North Korea.

    Args:
        input_path: a string representing the filepath of of the CSV of the
            dataframe that needs to be cleaned.
        output_path: name of file that the dataframe will save to (optional).
    Returns:
        Cleaned GDP dataframe.
    """
    gdp_total = pd.read_csv(input_path)

    # Drop unnecssary years
    gdp_total.drop(["2000", "2001", "2002", "2003", "2005", "2006", "2007",
                    "2009", "2010", "2011", "2013", "2014", "2015", "2017", "2018", "2019"],
                   axis=1, inplace=True)

    # Rename to include GDP in all column titles
    gdp_total.rename(columns={"Country (or dependent territory)": "Country",
                              "2004": "GDP-2004",
                              "2008": "GDP-2008",
                              "2012": "GDP-2012",
                              "2016": "GDP-2016"}, inplace=True)

    # Rename the UK and Taiwan to their olympic committee names
    gdp_total.replace({"United Kingdom": "Great Britain"}, inplace=True)
    gdp_total.replace({"Taiwan": "Chinese Taipei"}, inplace=True)

    # Use the UN's GDP per capita data for Cuba and North Korea
    # Source: https://en.wikipedia.org/wiki/List_of_countries_by_past_and_projec
    #         ted_GDP_(nominal)_per_capita#UN_estimates_between_2000_and_2009
    cuba_row = {"Country": "Cuba",
                "GDP-2004": 3399,
                "GDP-2008": 5386,
                "GDP-2012": 6448,
                "GDP-2016": 7657}
    gdp_total = gdp_total.append(cuba_row, ignore_index=True)
    north_korea_row = {"Country": "North Korea",
                       "GDP-2004": 473,
                       "GDP-2008": 551,
                       "GDP-2012": 643,
                       "GDP-2016": 642}
    gdp_total = gdp_total.append(north_korea_row, ignore_index=True)

    # If a location to save a csv is given, save it there
    if output_path is not None:
        gdp_total.to_csv(output_path, index=False)
    # Always return the dataframe
    return gdp_total


def scrape_athlete_table(url, table_num, year):
    """
    Convert the table on the wikipedia page for an olympic games that lists
    countries and how many athletes they sent in parentheses to a pandas
    dataframe.

    Also prefaces the column with number of athletes with a the year of the games.

    Args:
        url: a string representing the wikipedia page for the olympics games to
            scrape
        table_num: an int representing the index of the table that contains the
            relevant data
        year: an int or string representing the year of the olympic games page
            to be scraped so that the athlete count column can be properly named
    """
    response = requests.get(url)
    # Status code must be 200 to legally scrape
    if response.status_code == 200:
        # Get the html for the entire page
        whole_page = BeautifulSoup(response.text, "html.parser")
        # Make a list of all of the tables
        tables = whole_page.findAll("table", {"class": "wikitable"})
        # Get the correct table
        soup = tables[table_num]
        # Pull out all of the script and style to leave only visable text
        for script in soup(["script", "style"]):
            script.extract()
        text = soup.get_text()

        # Break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in
                  line.split("  "))
        # Drop blank lines and separate lines with ";"
        text = ";".join(chunk for chunk in chunks if chunk)
    else:
        print("Error: This table should not be scraped due to its status"
              " code.")

    # Decode from utf-8 so that country names are in same format as medaling,
    # population, and gdp data
    data = text.encode("utf-8")
    udata = data.decode("utf-8")
    text = str(udata.encode("ascii", "ignore"))

    # Remove host country indicator
    text = text.replace(" (host)", "")
    # Put a comma between the country name and the number of athletes sent
    # instead of parentheses
    text = text.replace("(", ",")
    # Remove unnecessary text and characters
    text = text.replace(")", "")
    text = text.replace("b'Participating National Olympic Committees;", "")
    text = text.replace("'", "")
    text = text.replace(" athletes", "")
    # Use regex to remove source references in square brackets
    text = re.sub(r"[\[].*?[\]]", "", text)

    # Read text into dataframe with commas separating values into columns and
    # semicolons indicating the start of a new row
    data_frame = pd.DataFrame([x.split(',') for x in text.split(';')])
    data_frame.rename(
        columns={0: "Country", 1: f"Athletes-{year}"}, inplace=True)

    return data_frame


def scrape_athlete_data(output_path=None):
    """
    Scrapes the number of athletes sent to the olympics by each country for the
    summer olympics 2004-2016 from Wikipedia and merges them into one dataframe.

    Args:
        output_path: name of file that the dataframe will save to (optional).
    Returns:
        The merged dataframe.
    """
    #                            Wikipedia page               Table on page
    pg_2004 = ["https://en.wikipedia.org/wiki/2004_Summer_Olympics", 1]
    pg_2008 = ["https://en.wikipedia.org/wiki/2008_Summer_Olympics", 5]
    pg_2012 = ["https://en.wikipedia.org/wiki/2012_Summer_Olympics", 1]
    pg_2016 = ["https://en.wikipedia.org/wiki/2016_Summer_Olympics", 2]

    # Scrape the tables that list the number of athletes competing for each
    # country on each summer olympics page 2004-2016
    df_2004 = scrape_athlete_table(pg_2004[0], pg_2004[1], 2004)
    df_2008 = scrape_athlete_table(pg_2008[0], pg_2008[1], 2008)
    df_2012 = scrape_athlete_table(pg_2012[0], pg_2012[1], 2012)
    df_2016 = scrape_athlete_table(pg_2016[0], pg_2016[1], 2016)

    # Merge the dataframes for each year into one
    all_athlete_dfs = [df_2004, df_2008, df_2012, df_2016]
    total = merge_dataframes(all_athlete_dfs)

    # If a location to save a csv is given, save it there
    if output_path is not None:
        total.to_csv(output_path, index=False)
    # Always return the dataframe
    return total


def merge_dataframes(df_list, output_path=None, method="left",
    merge_on="Country"):
    """
    Merge all dataframes in a list into one master dataframe by country.

        Args:
            df_list: a list of dataframes that should be merged
            output_path: name of file that the dataframe will save to (optional)
            method: a string representing what will used as the how arg for the
                pandas DataFrame merge() function (default: is "left" meaning
                keep all row in the datafram left of the one currently merging,
                and don't keep rows that don't match the reference column in
                the left dataframe)
            merge_on: a string representing what will used as the how arg for
                the pandas DataFrame merge() function (default: is "Country" meaning pandas will combine rows that have the same value in their column labeled "Country")
        Returns:
            The merged dataframe.s
    """
    # Initialize the master dataframe
    total = df_list[0]
    # Starting from the second, merge each dataframe into the ones before.
    for data_frame in df_list[1:]:
        total = total.merge(data_frame, how=method, left_on=merge_on, right_on=merge_on)

    # If a location to save a csv is given, save it there
    if output_path is not None:
        total.to_csv(output_path, index=False)
    # Always return the dataframe
    return total


def pivot(data_frame):
    """
    Pivot olympic dataframe into clean dataframe.

    Args:
        data_frame: pandas dataframe containing olympic data
    Returns:
        A dataframe containing the cleaned olympics data.
    """
    # creating new dataframe
    new_data = (
        data_frame
        # creating variable column with names of column and values to new column
        >> gr.tf_pivot_longer(
            columns=["Gold-2004", "Silver-2004", "Bronze-2004", "Total-2004",
                "GDP-2004", "Pop-2004", "Athletes-2004",
                "Gold-2008", "Silver-2008", "Bronze-2008", "Total-2008",
                "GDP-2008", "Pop-2008", "Athletes-2008",
                "Gold-2012","Silver-2012", "Bronze-2012", "Total-2012",
                "GDP-2012", "Pop-2012", "Athletes-2012",
                "Gold-2016", "Silver-2016", "Bronze-2016", "Total-2016",
                "GDP-2016", "Pop-2016", "Athletes-2016"],
            names_to=("Var"),
            values_to="val",
        )
        # separting type and year into two columns
        >> gr.tf_separate(
            column="Var",
            into=["Type", "Year"],
            sep="-",
        )
        # setting values to different types
        >> gr.tf_pivot_wider(
            names_from="Type",
            values_from="val"
        )
    )
    # creating success rate column for new dataframe
    new_data["Success Rate"] = new_data["Total"]/new_data["Athletes"]
    return new_data


def average_data(data_frame):
    """
    Creating averages dataframe from olympics data

    Args:
        data_frame: pandas dataframe containing olympic data
    Returns:
        A dataframe containing the averages of the olympics data.
    """
    # creating new dataframe
    new_data = pd.DataFrame()
    # setting country column as index
    new_data["Country"] = data_frame["Country"]
    # averaging all years and setting it to a new column
    new_data["Average Total"] = (data_frame["Total-2004"] +
                                    data_frame["Total-2008"] +
                                    data_frame["Total-2012"] +
                                    data_frame["Total-2016"]) / 4

    new_data["Average GDP"] = (data_frame["GDP-2004"] +
                                    data_frame["GDP-2008"] +
                                    data_frame["GDP-2012"] +
                                    data_frame["GDP-2016"]) / 4

    # multiplying by 1000 to standardize population
    new_data["Average Pop"] = (data_frame["Pop-2004"] +
                                    data_frame["Pop-2008"] +
                                    data_frame["Pop-2012"] +
                                    data_frame["Pop-2016"]) / 4

    new_data["Average Athletes"] = (data_frame["Athletes-2004"] +
                                    data_frame["Athletes-2008"] +
                                    data_frame["Athletes-2012"] +
                                    data_frame["Athletes-2016"]) / 4
    return new_data
