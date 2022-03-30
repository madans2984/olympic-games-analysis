import plotly.express as px

def medals_plot(df, sort, medal):
    if sort == "GDP":
        fig = px.scatter(
                         df,
                         x = df["GDP"],
                         y = df[f"{medal}"],
                         trendline="ols",
                         labels={f"{sort}" :"GDP (per capita) in dollars",
                                 f"{medal}" : f"{medal} Olympic medals"},
                         title=f"{sort} vs {medal} medals",
                         hover_data=["Country", "Year"],
                         log_x=False,
                         color = "Year"
                        )
    else:
        fig = px.scatter(
                         df,
                         x = df[f"{sort}"],
                         y = df[f"{medal}"],
                         trendline="ols",
                         labels={f"{sort}" : "Population (in thousands)",
                                 f"{medal}" : f"{medal} Olympic medals"},
                         title=f"{sort} vs {medal} medals",
                         hover_data=["Country", "Year"],
                         log_x=True,
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
                     color = "Year"
                    )
    fig.show()
    