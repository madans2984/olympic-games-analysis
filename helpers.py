import pandas as pd # library for data analysis
import requests # library to handle requests
from bs4 import BeautifulSoup # library to parse HTML documents
# get the response in the form of html
def table_scrape(url, index=0):
    """
    This functions takes a string representing the url of a wikipedia article and returns the first table on the page. If there are multiple tables and the return needs to be modified the index is an integer which represents the index of the table which needs to be scarped.
    
    Args:
        url: string representing the url of a wikipedia article
        index: index of the table on the wikipedia page
    """
    wikiurl=url
    table_class="wikitable sortable jquery-tablesorter"
    response=requests.get(wikiurl)
    if response.status_code == 200:
        # parse data from the html into a beautifulsoup object
        soup = BeautifulSoup(response.text, 'html.parser')
        tables=soup.findAll('table',{'class':"wikitable"})
        df=pd.read_html(str(tables[index]))
        # convert list to dataframe
        df=pd.DataFrame(df[0])
        return df
    else:
        print("Error: This table should not be scraped due to its status code.")

def medal_clean(df, year):
    """
    """
    df.rename(columns = {"Gold" : f"Gold-{year}", "Silver" : f"Silver-{year}", "Bronze" : f"Bronze-{year}", "Total" : f"Total-{year}"}, inplace = True)
    df.drop(["Rank"], axis = 1, inplace = True)
    df = df[:-1]
    return df