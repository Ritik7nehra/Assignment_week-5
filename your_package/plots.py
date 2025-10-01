import pandas as pd
import plotly.express as px

def make_scatter(df: pd.DataFrame, x: str, y: str):
    """Return a scatter plot figure."""
    fig = px.scatter(df, x=x, y=y, title=f"{y} vs {x}")
    return fig
