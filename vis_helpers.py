from ast import Index


def medals_plot(df, type, medal):
    import plotly.express as px
    if type == "GDP":
        fig = px.scatter(df, x = df["GDP"], y = df[f"{medal}"], trendline="ols", labels={f"{type}" : "GDP (per capita) in dollars", f"{medal}" : f"{medal} Olympic medals"}, title=f"{type} vs {medal} medals", hover_data=["Country", "Year"], log_x=False, color = "Year")
    else:
        fig = px.scatter(df, x = df[f"{type}"], y = df[f"{medal}"], trendline="ols", labels={f"{type}" : "Population (in thousands)", f"{medal}" : f"{medal} Olympic medals"}, title=f"{type} vs {medal} medals", hover_data=["Country", "Year"], log_x=True, color = "Year")
    fig.show()

def medals_plot_year(df, year, type, medal):
    """
    """
    import plotly.express as px
    if type == "GDP":
        fig = px.scatter(df, x = df[f"{type}-{year}"], y = df[f"{medal}-{year}"], trendline="ols", labels={f"{type}-{year}" : "GDP (per capita) in dollars", f"{medal}-{year}" : f"{medal} Olympic medals"}, title=f"{type} vs {medal} medals in {year}", hover_data=['Country'], log_x=False)
    else:
        fig = px.scatter(df, x = df[f"{type}-{year}"], y = df[f"{medal}-{year}"], trendline="ols", labels={f"{type}-{year}" : "Population (in thousands)", f"{medal}-{year}" : f"{medal} Olympic medals"}, title=f"{type} vs {medal} medals in {year}", hover_data=['Country'], log_x=True)
    fig.show()

def context_plot(df, year, type1="GDP", type2="Pop"):
    """
    """
    import plotly.express as px
    fig = px.scatter(df, x = df[f"{type2}-{year}"], y = df[f"{type1}-{year}"], trendline="ols", labels={f"{type1}-{year}" : "GDP (per capita) in dollars", f"{type2}-{year}" : "Population (in thousands)"}, title=f"GDP (per capita) vs population in {year}", hover_data=['Country'], log_x=True, log_y=True)
    fig.show()
    