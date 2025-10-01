import plotly.express as px
import pandas as pd

# update/add code below ...
import pandas as pd
import plotly.express as px

# Load Titanic dataset once here (so functions can access it)
df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')


def visualize_demographic():
    """
    Show passenger demographics (Sex vs Survival).
    """
    fig = px.histogram(
        df,
        x="Sex",
        color="Survived",
        barmode="group",
        title="Survival by Sex"
    )
    return fig


def visualize_families():
    """
    Show survival depending on family aboard (SibSp + Parch).
    """
    df_copy = df.copy()
    df_copy["Family"] = df_copy["SibSp"] + df_copy["Parch"]

    fig = px.histogram(
        df_copy,
        x="Family",
        color="Survived",
        barmode="group",
        title="Survival by Family Count"
    )
    return fig


def visualize_family_size():
    """
    Show survival rates by family size categories.
    """
    df_copy = df.copy()
    df_copy["FamilySize"] = df_copy["SibSp"] + df_copy["Parch"] + 1

    df_copy["FamilyCategory"] = pd.cut(
        df_copy["FamilySize"],
        bins=[0, 1, 4, 20],
        labels=["Alone", "Small (2-4)", "Large (5+)"]
    )

    fig = px.histogram(
        df_copy,
        x="FamilyCategory",
        color="Survived",
        barmode="group",
        title="Survival by Family Size Category"
    )
    return fig
