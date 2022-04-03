import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
import re
import grama as gr # library for data cleaning
# get the response in the form of html
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
    wikiurl = url
    table_class = "wikitable sortable jquery-tablesorter"
    response = requests.get(wikiurl)
    # status code must be 200 to legally scrape
    if response.status_code == 200:
        # Parse data from the html into a beautifulsoup object
        soup = BeautifulSoup(response.text, "html.parser")
        tables=soup.findAll("table",{"class": "wikitable"})
        df=pd.read_html(str(tables[index]))
        # Convert list to dataframe
        df=pd.DataFrame(df[0])
        return df
    else:
        print("Error: This table should not be scraped due to its status" \
              " code.")


def scrape_medal_table(url, year, host):
    """
    Convert the medal table on the wikipedia page for an olympic games to a
    pandas dataframe.

    Makes each column (other than "Country") preface with the year of the games.
    """
    table = table_scrape(url)
    # renaming columns to have the year in the title
    table.rename(columns = {"NOC": "Country", "Nation": "Country", "Gold": f"Gold-{year}", "Silver": f"Silver-{year}",
        "Bronze": f"Bronze-{year}", "Total": f"Total-{year}"}, inplace = True)
    # dropping rank column because it's not relevant for our question
    table.drop(["Rank"], axis = 1, inplace = True)
    table.replace({f"{host}*" : f"{host}"}, inplace = True)
    table[f"Weighted-{year}"] = table[f"Gold-{year}"] * 3 + table[f"Silver-{year}"] * 2 + table[f"Bronze-{year}"] * 1

    # removing final row containing total number of countries
    table = table[:-1]
    return table


def scrape_medal_data(output_path=None, include_NaNs=True):
    '''
    Scrapes medal data for desired years from Wikipedia and merges them into
    one dataframe.
    
    Args:
        output_path: name of file dataframe is saved to.
    
    Returns:
        The merged dataframe.
    '''
    pg_2004 = "https://en.m.wikipedia.org/wiki/2004_Summer_Olympics_medal_table"
    pg_2008 = "https://en.m.wikipedia.org/wiki/2008_Summer_Olympics_medal_table"
    pg_2012 = "https://en.m.wikipedia.org/wiki/2012_Summer_Olympics_medal_table"
    pg_2016 = "https://en.wikipedia.org/wiki/2016_Summer_Olympics_medal_table"
    medals_2004 = scrape_medal_table(pg_2004, "2004", "Greece")
    medals_2008 = scrape_medal_table(pg_2008, "2008", "China")
    medals_2012 = scrape_medal_table(pg_2012, "2012", "Great Britain")
    medals_2016 = scrape_medal_table(pg_2016, "2016", "Brazil")

    if include_NaNs:
        merge_method = "outer"
    else:
        merge_method = "inner"

    medals_all = medals_2012.merge(medals_2008, how=merge_method,
        left_on="Country", right_on="Country")
    medals_all = medals_all.merge(medals_2016, how=merge_method,
        left_on="Country", right_on="Country")
    medals_all = medals_all.merge(medals_2004, how=merge_method,
        left_on="Country", right_on="Country")

    if output_path != None:
        medals_all.to_csv(output_path, index=False)
    return medals_all

def clean_medal_data(path_orig, output_path=None):
    '''
    Clean the medal data by removing data for Independent Olympic Athletes.
    
    Args:
        path_orig: path of dataframe to clean.
        output_path: name of file dataframe is saved to.

    Returns:
        The cleaned medal data dataframe.
    '''
    medals = pd.read_csv(path_orig)
    # independents_index = medals.index[medals['Country'] == "Independent Olympic Athletes"].item()
    # medals.drop(independents_index, axis = 0, inplace = True)
    medals = medals.fillna(0)

    if output_path != None:
        medals.to_csv(output_path, index=False)
    return medals

def scrape_population_data(output_path=None):
    '''
    Scrape population data from wikipedia.
    
    Args:
        output_path: name of file dataframe is saved to.
    
    Returns:
        Dataframe containing scraped population data.
    '''
    wikipedia_page = ("https://en.wikipedia.org/wiki/List_of_countries_by_past_"
    "and_projected_future_population#Estimates_between_the_years_1985_and_2015_"
    "(in_thousands)")
    population = table_scrape(wikipedia_page, 1)
    if output_path != None:
        population.to_csv(output_path, index=False)
    return population


def clean_population_data(filepath_original, filepath_result=None):
    '''
    Clean population data from wikipedia by removing unnecessary years and
    percentages of population to leave whole numbers.
    
    The closest years' population was used for each year of the Olympics (i.e. population data in 2005 was used for the Olympic Games in 2004, population data in 2010 was used for the Games in both 2008 and 2010, and population data in 2015 was used for 2016. Population columns were renamed to correspond with Olympic Games' years. Special cases: renamed Great Britain as United Kingdom and Chinese Taipei as Taiwan, as well as added a new row with the summed populations of Serbia and Montenegro because they compete jointly.
    
    Args:
        output_path: name of file dataframe is saved to.
    
    Returns:
        The cleaned population dataframe.
    '''
    population = pd.read_csv(filepath_original)
    # dropping unnecessary years
    population.drop(["1985", "1990", "1995", "2000", "%", "%.1", "%.2", "%.3", "%.4","%.5", "%.6"], axis = 1, inplace = True)
    # renaming columns to be associate with the correct olympic years
    population.rename(columns = {"Country (or dependent territory)":"Country",
        "2005": "Pop-2004",
        "2010": "Pop-2008",
        "2015": "Pop-2016"}, inplace = True)
    # creating a column for the population in 2012 and duplicating 2008 into it
    population["Pop-2012"] = population["Pop-2008"]
    # reordering population dataframe to be chronological
    population = population[["Country", "Pop-2004", "Pop-2008", "Pop-2012",
        "Pop-2016"]]

    population.replace({"United Kingdom" : "Great Britain"}, inplace = True)
    population.replace({"Taiwan" : "Chinese Taipei"}, inplace = True)

    s_m_row = make_sum_row(population, "Serbia", "Montenegro")
    population = population.append(s_m_row, ignore_index=True)

    if filepath_result != None:
        population.to_csv(filepath_result, index=False)
    return population


def scrape_gdp_data(output_path=None):
    '''
    Scrape the IMF's GDP per capita data from wikipedia.
    
    Args:
        output_path: name of file dataframe is saved to.
    
    Returns:
        A dataframe containing the scraped GDP data.
    '''
    wikipedia_page = ("https://en.wikipedia.org/wiki/"
        "List_of_countries_by_past_and_projected_GDP_(PPP)_per_capita")
    gdp_2000s = table_scrape(wikipedia_page, 2)
    gdp_2010s = table_scrape(wikipedia_page, 3)
    gdp_total = gdp_2000s.merge(gdp_2010s,how="left",
        left_on="Country (or dependent territory)",
        right_on="Country (or dependent territory)")
    if output_path != None:
        gdp_total.to_csv(output_path, index=False)
    return gdp_total


def clean_gdp_data(path_orig, path_result=None, clean_pop_data_path=None):
    '''
    Clean GDP data by dropping unnecessary years, renaming columns, and adding
    missing competitors. 
    
    Special cases: renamed Great Britain as United Kingdom and Chinese Taipei
    as Taiwan; use the UN's GDP per capita for Cuba and North Korea; get
    weighted averages of GDP per capita values for Serbia and Monetenegro to
    combine into single value per year.
    
    Args:
        clean_pop_data_path: path of cleaned dataframe:
        path_orig: path of dataframe if not already cleaned.
        path_result: name of file dataframe is saved to.

    Returns:
        Cleaned GDP dataframe.
    '''
    gdp_total = pd.read_csv(path_orig)
    if clean_pop_data_path == None:
        population = clean_population_data("data/population_original.csv")
    else:
        population = pd.read_csv(clean_pop_data_path)

    # dropping unnecssary years
    gdp_total.drop(["2000", "2001", "2002", "2003", "2005", "2006", "2007",
        "2009","2010", "2011", "2013", "2014", "2015", "2017", "2018", "2019"],
        axis = 1, inplace = True)

    # renaming to include GDP in all column titles
    gdp_total.rename(columns = {"Country (or dependent territory)":"Country",
        "2004": "GDP-2004",
        "2008": "GDP-2008",
        "2012": "GDP-2012",
        "2016": "GDP-2016"}, inplace = True)

    # Rename the UK and Taiwan to the names they compete in the olympics under
    gdp_total.replace({"United Kingdom" : "Great Britain"}, inplace = True)
    gdp_total.replace({"Taiwan" : "Chinese Taipei"}, inplace = True)

    # Use the UN's GDP per capita data for Cuba and North Korea
    # Source: https://en.wikipedia.org/wiki/List_of_countries_by_past_and_projec
    #         ted_GDP_(nominal)_per_capita#UN_estimates_between_2000_and_2009
    cuba_row = {"Country":"Cuba",
        "GDP-2004": 3399,
        "GDP-2008": 5386,
        "GDP-2012": 6448,
        "GDP-2016": 7657}
    gdp_total = gdp_total.append(cuba_row, ignore_index=True)
    north_korea_row = {"Country":"North Korea",
        "GDP-2004": 473,
        "GDP-2008": 551,
        "GDP-2012": 643,
        "GDP-2016": 642}
    gdp_total = gdp_total.append(north_korea_row, ignore_index=True)

    s_m_row = make_weighted_ave_row(population, gdp_total, 
        "Serbia", "Montenegro")
    gdp_total = gdp_total.append(s_m_row, ignore_index=True)

    if path_result != None:
        gdp_total.to_csv(path_result, index=False)
    return gdp_total

# def make_sum_row(dataframe, country1_name, country2_name):
#     col_list = list(dataframe.columns)[1:]
#     country1 = dataframe.loc[dataframe["Country"] == country1_name]
#     country2 = dataframe.loc[dataframe["Country"] == country2_name]
#     new_name = country1_name + " and " + country2_name
#     new_row = {"Country":new_name}
#     for col in col_list:
#         new_row[col] = country1[col].item() + country2[col].item()
#     return new_row

# def make_weighted_ave_row(weights_df, vals_df, country1_name, country2_name):
#     weights_col_list = list(weights_df.columns)[1:]
#     vals_col_list = list(vals_df.columns)[1:]
#     country1_weights = weights_df.loc[weights_df["Country"] == country1_name]
#     country2_weights = weights_df.loc[weights_df["Country"] == country2_name]
#     country1_vals = vals_df.loc[vals_df["Country"] == country1_name]
#     country2_vals = vals_df.loc[vals_df["Country"] == country2_name]
#     new_name = country1_name + " and " + country2_name
#     new_row = {"Country":new_name}
#     for weight_col, val_col in zip(weights_col_list, vals_col_list):
#         weight1 = country1_weights[weight_col].item()
#         val1 = country1_vals[val_col].item()
#         weight2 = country2_weights[weight_col].item()
#         val2 = country2_vals[val_col].item()
#         new_row[val_col] = (weight1*val1 + weight2*val2)//(val1+val2)
#     return new_row

def scrape_athlete_table(url, table_num, year):
    response = requests.get(url)
    # status code must be 200 to legally scrape
    if response.status_code == 200:
        whole_page = BeautifulSoup(response.text, "html.parser")
        tables = whole_page.findAll("table",{"class": "wikitable"})
        soup = tables[table_num]
        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = ';'.join(chunk for chunk in chunks if chunk)
    else:
        print("Error: This table should not be scraped due to its status" \
          " code.")

    text = text.replace(" (host)","")
    text = text.replace("(",",")
    text = text.replace(")","")
    text = text.replace("Participating National Olympic Committees;","")
    text = text.replace("'","")
    text = text.replace(" athletes","")

    text = re.sub("[\(\[].*?[\)\]]", "", text)

    df = pd.DataFrame([x.split(',') for x in text.split(';')])
    df.rename(columns = {0: "Country", 1: f"Athletes-{year}"}, inplace = True)

    return df

def scrape_athlete_data(output_path=None):
    pg_2004 = ["https://en.wikipedia.org/wiki/2004_Summer_Olympics", 1]
    pg_2008 = ["https://en.wikipedia.org/wiki/2008_Summer_Olympics", 5]
    pg_2012 = ["https://en.wikipedia.org/wiki/2012_Summer_Olympics", 1]
    pg_2016 = ["https://en.wikipedia.org/wiki/2016_Summer_Olympics", 2]

    df_2004 = scrape_athlete_table(pg_2004[0], pg_2004[1], 2004)
    df_2008 = scrape_athlete_table(pg_2008[0], pg_2008[1], 2008)
    df_2012 = scrape_athlete_table(pg_2012[0], pg_2012[1], 2012)
    df_2016 = scrape_athlete_table(pg_2016[0], pg_2016[1], 2016)

    all_athlete_dfs = [df_2004, df_2008, df_2012, df_2016]
    total = merge_dataframes(all_athlete_dfs)

    if output_path != None:
        total.to_csv(output_path, index=False)
    return total


def merge_data(medals_df, pop_df, gdp_df, output_path=None):
    '''
    Merge medals, population, and gdp data into single dataframe based on
    country.
    
    Args:
        medals_df: dataframe with medals data.
        pop_df: dataframe with population data.
        gdp_df: dataframe with GDP per capita data.
        output_path: name of file dataframe is saved to.
    
    Returns:
        total: the merged dataframe.
    '''
    total = medals_df.merge(gdp_df,how="left",left_on="Country",right_on="Country")
    total = total.merge(pop_df,how="left",left_on="Country",right_on="Country")

    if output_path != None:
        total.to_csv(output_path, index=False)
    return total


def merge_dataframes(df_list, output_path=None, method="left", on="Country"):
    total = df_list[0]
    for df in df_list[1:]:
        total = total.merge(df, how=method, left_on=on, right_on = on)
    
    if output_path != None:
        total.to_csv(output_path, index=False)
    return total


def pivot(new_data, data_frame):
    new_data = (
    data_frame
    >> gr.tf_pivot_longer(
        columns=["Gold-2004", "Silver-2004", "Bronze-2004", "Total-2004", "Weighted-2004", "GDP-2004", "Pop-2004", "Athletes-2004",
                 "Gold-2008", "Silver-2008", "Bronze-2008", "Total-2008", "Weighted-2008", "GDP-2008", "Pop-2008", "Athletes-2008",
                 "Gold-2012", "Silver-2012", "Bronze-2012", "Total-2012", "Weighted-2012", "GDP-2012", "Pop-2012", "Athletes-2012",
                 "Gold-2016", "Silver-2016", "Bronze-2016", "Total-2016", "Weighted-2016", "GDP-2016", "Pop-2016", "Athletes-2016"],
        names_to=("Var"),
        values_to="val",
    )
    >> gr.tf_separate(
        column="Var",
        into=["Type", "Year"],
        sep="-",
    )
    >> gr.tf_pivot_wider(
        names_from = "Type",
        values_from = "val"
    )
)
    new_data["Success Rate"] = new_data["Total"]/new_data["Athletes"]

def average_data(new_data, data_frame):
    new_data = pd.DataFrame()
    new_data["Country"] = data_frame["Country"]
    new_data["Average Total"] = (data_frame[f"Total-2004"] + data_frame["Total-2008"] + data_frame["Total-2012"] + data_frame["Total-2016"]) / 4
    new_data["Average GDP"] = (data_frame[f"GDP-2004"] + data_frame["GDP-2008"] + data_frame["GDP-2012"] + data_frame["GDP-2016"]) / 4
    new_data["Average Pop"] = (data_frame[f"Pop-2004"] + data_frame["Pop-2008"] + data_frame["Pop-2012"] + data_frame["Pop-2016"]) / 4 * 1000
    new_data["Average Athletes"] = (data_frame[f"Athletes-2004"] + data_frame["Athletes-2008"] + data_frame["Athletes-2012"] + data_frame["Athletes-2016"]) / 4
