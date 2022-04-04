# olympic-games-analysis
Analysis of Olympic performance and its correlation with a country's GDP per capita and population size
test edit

### Summary:
We explored the correlations between the number of medals a country won in the years 2004-2016 at the Summer Olympics and the country's GDP and population. We later expanded the scope of this project to also include the number of athletes which a country sent in the given year. While the project also contains the data to visulise and model specific medal categories (Gold, Silver, Bronze), this isn't further explored in this project.

### Data Collecting Instructions:
We used beautifulsoup to scrape multiple wikitables for our data. While our links are coded in for 2004-2016, searching the medal table for a particular year will give you the data needed to adapt this project to other Olympic years.

### Plotting and Modeling Instructions:
The plotting and modeling functions are coded into the vis_helpers.py file. In that file, we have outlined the specific inputs need in order to get similar plots to ours. The key here is to use the correct data form (for example, an averaged data table versus a pivoted data table). We used py-grama and plotly to do this and those functions are also included.

### Installation:

plotly
'''
pip install plotly
'''
grama
'''
pip install py-grama
'''
statsmodels
'''
pip install statsmodels
'''
requests
'''
pip install requests
'''
bs4
'''
pip install bs4
'''