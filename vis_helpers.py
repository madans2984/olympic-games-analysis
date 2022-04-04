import plotly.express as px
import statsmodels.formula.api as smf


def medals_plot(df, sort, medal):
    if sort == "GDP":
        fig = px.scatter(
                         df,
                         x = df["GDP"],
                         y = df[f"{medal}"],
                         trendline="ols",
                         labels={f"{sort}" :"GDP (per capita) in dollars",
                                 f"{medal}" : f"{medal} Olympic medals"},
                         title=f"GDP (per capita) vs {medal} medals",
                         hover_data=["Country", "Year"],
                         log_x=False,
                         color = "Year",
                         facet_col = "Year"
                        )
    elif sort == "Pop":
        fig = px.scatter(
                         df,
                         x = df["Pop"],
                         y = df[f"{medal}"],
                         trendline="ols",
                         labels={f"{sort}" : "Population (in thousands)",
                                 f"{medal}" : f"{medal} Olympic medals"},
                         title=f"Population vs {medal} medals",
                         hover_data=["Country", "Year"],
                         log_x=True,
                         color = "Year",
                         facet_col = "Year"
                        )
    else:
        fig = px.scatter(
                 df,
                 x = df["Athletes"],
                 y = df[f"{medal}"],
                 trendline="ols",
                 labels={"Athletes" :"Total Number of Competitors",
                 f"{medal}" : f"{medal} Number of Medals"},
                 title=f"Number of Competitors vs Number of {medal} Medals",
                 hover_data=["Country"],
                 log_x=True,
                 facet_col= "Year",
                 color = "Year"
                )    
    fig.show()


def context_plot(df, sort1="GDP", sort2="Pop"):
    """
    """
    fig = px.scatter(
                     df,
                     x = df[f"{sort2}"],
                     y = df[f"{sort1}"],
                     trendline="ols",
                     labels={f"{sort1}" : "GDP (per capita) in dollars",
                             f"{sort2}" : "Population (in thousands)"},
                     title=f"GDP (per capita) vs population",
                     hover_data=["Country"],
                     log_x=True,
                     log_y=False,
                     color = "Year",
                     facet_col = "Year"
                    )
    fig.show()
    
def model_check(data_frame, equation):
        mod = smf.ols(formula=f"{equation}", data=data_frame)
        res = mod.fit()
        print(res.summary())