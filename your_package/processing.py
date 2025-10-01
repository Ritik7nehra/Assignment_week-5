import pandas as pd

def summarize_by_group(df: pd.DataFrame, group_col: str, value_col: str):
    """Return mean of value_col grouped by group_col."""
    return df.groupby(group_col)[value_col].mean().reset_index()
