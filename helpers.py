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
    # Status code must be 200 to legally scrape
    if response.status_code == 200:
        # Parse data from the html into a beautifulsoup object
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.findAll('table',{'class':"wikitable"})
        df = pd.read_html(str(tables[index]))
        # Convert list to dataframe
        df = pd.DataFrame(df[0])
        return df
    else:
        print("Error: This table should not be scraped due to its status" \
              " code.")

def medal_clean(df, year, host):
    """
    This functions takes in a data frame of the medals tables from wikipedia
    and cleans it to be easier to read.

    Args:
        df: data frame containing medals table from wikipedia
        year: integer representing the year of the olympic games

    Returns:
        cleaned dataframe
    """
    # renaming columns to have the year in the title
    df.rename(columns = {"Gold" : f"Gold-{year}", "Silver" : f"Silver-{year}",
                         "Bronze" : f"Bronze-{year}",
                         "Total" : f"Total-{year}"}, inplace = True)
    # dropping rank column because it's not relevant for our question
    df.drop(["Rank"], axis = 1, inplace = True)
    df.replace({f"{host}*" : f"{host}"}, inplace = True)
    # removing final row containing total number of countries
    df = df[:-1]
    return df