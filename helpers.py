import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
# get the response in the form of html
def table_scrape(url, index=0):
    """
    This functions takes a string representing the url of a wikipedia article
    and by default returns the first table on the page. If there are multiple
    tables and the return needs to be modified the index is an integer which
    represents the index of the table which needs to be scraped.

    Args:
        url: string representing the url of a wikipedia article
        index: index of the table on the wikipedia page

    Returns:
        pandas dataframe consisting of data in the wikitable
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

# def medal_clean(df, year, host):
#     """
#     This functions takes in a data frame of the medals tables from wikipedia
#     and cleans it to be easier to read.

#     Args:
#         df: data frame containing medals table from wikipedia
#         year: integer representing the year of the olympic games

#     Returns:
#         cleaned dataframe
#     """
#     # renaming columns to have the year in the title
#     df.rename(columns = {"Gold": f"Gold-{year}", "Silver": f"Silver-{year}",
#         "Bronze": f"Bronze-{year}", "Total": f"Total-{year}"}, inplace = True)
#     # dropping rank column because it's not relevant for our question
#     df.drop(["Rank"], axis = 1, inplace = True)
#     df.replace({f"{host}*" : f"{host}"}, inplace = True)
#     df[f"Weighted-{year}"] = df[f"Gold-{year}"] * 3 + df[f"Silver-{year}"] * 2 + df[f"Bronze-{year}"] * 1

#     # removing final row containing total number of countries
#     df = df[:-1]
#     return df

def scrape_medal_table(url, year, host):
    """
    Convert the medal table on the wikipedia page for an olympic games to a pandas dataframe.

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
    medals = pd.read_csv(path_orig)
    # independents_index = medals.index[medals['Country'] == "Independent Olympic Athletes"].item()
    # medals.drop(independents_index, axis = 0, inplace = True)
    medals = medals.fillna(0)

    if output_path != None:
        medals.to_csv(output_path, index=False)
    return medals

def scrape_population_data(output_path=None):
    wikipedia_page = ("https://en.wikipedia.org/wiki/List_of_countries_by_past_"
    "and_projected_future_population#Estimates_between_the_years_1985_and_2015_"
    "(in_thousands)")
    population = table_scrape(wikipedia_page, 1)
    if output_path != None:
        population.to_csv(output_path, index=False)
    return population


def clean_population_data(filepath_original, filepath_result=None):
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
    gdp_total = pd.read_csv(path_orig)
    if clean_pop_data_path == None:
        population = clean_population_data("population_original.csv")
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

def make_sum_row(dataframe, country1_name, country2_name):
    col_list = list(dataframe.columns)[1:]
    country1 = dataframe.loc[dataframe["Country"] == country1_name]
    country2 = dataframe.loc[dataframe["Country"] == country2_name]
    new_name = country1_name + " and " + country2_name
    new_row = {"Country":new_name}
    for col in col_list:
        new_row[col] = country1[col].item() + country2[col].item()
    return new_row

def make_weighted_ave_row(weights_df, vals_df, country1_name, country2_name):
    weights_col_list = list(weights_df.columns)[1:]
    vals_col_list = list(vals_df.columns)[1:]
    country1_weights = weights_df.loc[weights_df["Country"] == country1_name]
    country2_weights = weights_df.loc[weights_df["Country"] == country2_name]
    country1_vals = vals_df.loc[vals_df["Country"] == country1_name]
    country2_vals = vals_df.loc[vals_df["Country"] == country2_name]
    new_name = country1_name + " and " + country2_name
    new_row = {"Country":new_name}
    for weight_col, val_col in zip(weights_col_list, vals_col_list):
        weight1 = country1_weights[weight_col].item()
        val1 = country1_vals[val_col].item()
        weight2 = country2_weights[weight_col].item()
        val2 = country2_vals[val_col].item()
        new_row[val_col] = (weight1*val1 + weight2*val2)//(val1+val2)
    return new_row


def merge_data(medals_df, pop_df, gdp_df, output_path=None):
    total = medals_df.merge(gdp_df,how="left",left_on="Country",right_on="Country")
    total = total.merge(pop_df,how="left",left_on="Country",right_on="Country")

    if output_path != None:
        total.to_csv(output_path, index=False)
    return total