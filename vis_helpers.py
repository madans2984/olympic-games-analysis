"""
Functions for plotting and creating models
"""

import plotly.express as px
import statsmodels.formula.api as smf


def medals_plot(data_frame, sort, medal):
    """
    Creates plots from pandas dataframe with a particular type of medal category and a comparative
    factor.

    Args:
        data_frame: pandas dataframe containing information
        sort: comparative factor ("GDP", "Pop", "Athletes)
        medal: medal category ("Gold", "Silver", "Bronze", "Total", "Success Rate")

    Returns:
        A plotly figure of the input information.
    """
    if sort == "GDP":
        # creating specific labels for GDP per capita graphs
        fig = px.scatter(
            data_frame,
            x=data_frame["GDP"],
            y=data_frame[f"{medal}"],
            trendline="ols",
            labels={f"{sort}": "GDP (per capita) in dollars",
                    f"{medal}": f"{medal} Olympic medals"},
            title=f"GDP (per capita) vs {medal} medals",
            hover_data=["Country", "Year"],
            log_x=False,
            color="Year",
            facet_col="Year"
        )
    elif sort == "Pop":
        # creating specific labels for Pop graphs
        fig = px.scatter(
            data_frame,
            x=data_frame["Pop"],
            y=data_frame[f"{medal}"],
            trendline="ols",
            labels={f"{sort}": "Population (in thousands)",
                    f"{medal}": f"{medal} Olympic medals"},
            title=f"Population vs {medal} medals",
            hover_data=["Country", "Year"],
            log_x=True,
            color="Year",
            facet_col="Year"
        )
    else:
        # creating specific labels for Athletes graphs
        fig = px.scatter(
            data_frame,
            x=data_frame["Athletes"],
            y=data_frame[f"{medal}"],
            trendline="ols",
            labels={"Athletes": "Total Number of Competitors",
                    f"{medal}": f"{medal} Number of Medals"},
            title=f"Number of Competitors vs Number of {medal} Medals",
            hover_data=["Country"],
            log_x=True,
            facet_col="Year",
            color="Year"
        )
    fig.show()


def context_plot(data_frame, sort1="GDP", sort2="Pop"):
    """
    Creates plots from pandas dataframe containing GDP and Pop.

    Args:
        sort1: context factor 1 ("GDP", "Pop")
        sort2: context factor 2 ("GDP", "Pop")

    Returns:
        A plotly figure of the input information.
    """
    # creating plot contextualizing GDP per capita and population
    fig = px.scatter(
        data_frame,
        x=data_frame[f"{sort2}"],
        y=data_frame[f"{sort1}"],
        trendline="ols",
        labels={f"{sort1}": "GDP (per capita) in dollars",
                f"{sort2}": "Population (in thousands)"},
        title="GDP (per capita) vs population",
        hover_data=["Country"],
        log_x=True,
        log_y=False,
        color="Year",
        facet_col="Year"
    )
    fig.show()


def model_check(data_frame, equation):
    """
    Returns model fit statistics

    Args:
        data_frame: pandas dataframe containing information
        equation: formula for creating model

    Returns:
        Summary of model fit statistics.
    """
    # creating model
    mod = smf.ols(formula=f"{equation}", data=data_frame)
    res = mod.fit()
    # printing summary of model fit stats
    print(res.summary())


def average_medals_plot(data_frame, sort, medal):
    """
    Creates plots from pandas dataframe with a particular type of medal category and a comparative
    factor.

    Args:
        data_frame: pandas dataframe containing information
        sort: comparative factor ("Average GDP", "Average Pop", "Average Athletes)
        medal: medal category ("Average Total")

    Returns:
        A plotly figure of the input information.
    """
    if sort == "Average GDP":
        # creating specific labels for average GDP per capita graphs
        fig = px.scatter(
            data_frame,
            x=data_frame["Average GDP"],
            y=data_frame[f"{medal}"],
            trendline="ols",
            labels={f"{sort}": "Average GDP (per capita) in dollars",
                    f"{medal}": f"{medal} Olympic medals"},
            title=f"Average GDP (per capita) vs {medal} medals from 2004-2016",
            hover_data=["Country"],
            log_x=False,
        )
    elif sort == "Average Pop":
        # creating specific labels for average pop graphs
        fig = px.scatter(
            data_frame,
            x=data_frame["Average Pop"],
            y=data_frame[f"{medal}"],
            trendline="ols",
            labels={f"{sort}": "Average Population from 2005-2015",
                    f"{medal}": f"{medal} Olympic medals"},
            title=f"Average Population vs {medal} medals from 2004-2016",
            hover_data=["Country"],
            log_x=True,
        )
    else:
        # creating specific labels for average athletes graphs
        fig = px.scatter(
            data_frame,
            x=data_frame["Average Athletes"],
            y=data_frame[f"{medal}"],
            trendline="ols",
            labels={"Athletes": "Average Total Number of Competitors",
                    f"{medal}": f"{medal} Number of Medals"},
            title=f"Average Number of Competitors vs Average Number of {medal} Medals",
            hover_data=["Country"],
            log_x=True
        )
    fig.show()


def average_context_plot(data_frame, sort1="Average GDP", sort2="Average Pop"):
    """
    Creates plots from pandas dataframe containing GDP and Pop.

    Args:
        sort1: context factor 1 ("Average GDP", "Average Pop")
        sort2: context factor 2 ("Average GDP", "Average Pop")

    Returns:
        A plotly figure of the input information.
    """
    # creating plot contextualizing average GDP per capita and average population
    fig = px.scatter(
        data_frame,
        x=data_frame[f"{sort2}"],
        y=data_frame[f"{sort1}"],
        trendline="ols",
        labels={f"{sort1}": "Average GDP (per capita) in dollars",
                f"{sort2}": "Average Population from 2005-2015"},
        title="Average GDP (per capita) vs Average Population from 2004-2016",
        hover_data=["Country"],
        log_x=True,
    )
    fig.show()
