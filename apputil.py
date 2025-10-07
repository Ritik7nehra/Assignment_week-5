# apputil.py
import pandas as pd
import plotly.express as px
from typing import Optional

# source CSV (same URL you used in app.py)
TITANIC_CSV = 'https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv'

def load_titanic() -> pd.DataFrame:
    """Load Titanic data (single place so all functions share the same source)."""
    return pd.read_csv(TITANIC_CSV)


def survival_demographics(df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """
    Exercise 1: Return a table grouped by Pclass, Sex, AgeGroup with:
      - n_passengers
      - n_survivors
      - survival_rate (0-1)
    Age groups: Child (<=12), Teen (13-19), Adult (20-59), Senior (60+), Unknown
    """
    if df is None:
        df = load_titanic()
    df2 = df.copy()

    # Create age groups; keep Unknown for missing ages
    bins = [-0.1, 12, 19, 59, 200]  # use -0.1 to include 0-year-olds when present
    labels = ['Child', 'Teen', 'Adult', 'Senior']
    df2['AgeGroup'] = pd.cut(df2['Age'], bins=bins, labels=labels)
    # add Unknown category and fill NaN with 'Unknown'
    df2['AgeGroup'] = df2['AgeGroup'].cat.add_categories('Unknown').fillna('Unknown')
    # Make ordering explicit (helps sorting and plotting)
    df2['AgeGroup'] = pd.Categorical(df2['AgeGroup'],
                                     categories=labels + ['Unknown'],
                                     ordered=True)

    # Group and aggregate
    grouped = df2.groupby(['Pclass', 'Sex', 'AgeGroup'], observed=True)
    summary = grouped['Survived'].agg(
        n_passengers='count', n_survivors='sum'
    ).reset_index()
    summary['survival_rate'] = summary['n_survivors'] / summary['n_passengers']

    # Sort for readability: Pclass (1,2,3), Sex (female, male), AgeGroup (Child..Unknown)
    # Ensure consistent ordering for Pclass and Sex for human-readable tables
    summary['Pclass'] = pd.Categorical(summary['Pclass'],
                                       categories=sorted(df2['Pclass'].unique()),
                                       ordered=True)
    sex_order = ['female', 'male'] if set(['female','male']).issubset(set(df2['Sex'].unique())) else sorted(df2['Sex'].unique())
    summary['Sex'] = pd.Categorical(summary['Sex'], categories=sex_order, ordered=True)

    summary = summary.sort_values(['Pclass', 'Sex', 'AgeGroup']).reset_index(drop=True)
    return summary


def family_groups(df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """
    Exercise 2: Create family_size = SibSp + Parch + 1, then group by family_size and Pclass.
    Return columns:
      - family_size
      - Pclass
      - n_passengers
      - avg_fare
      - min_fare
      - max_fare
    Sorted by Pclass then family_size.
    """
    if df is None:
        df = load_titanic()
    df2 = df.copy()

    # Ensure numeric, fill missing SibSp/Parch with 0
    df2['SibSp'] = pd.to_numeric(df2['SibSp'], errors='coerce').fillna(0).astype(int)
    df2['Parch'] = pd.to_numeric(df2['Parch'], errors='coerce').fillna(0).astype(int)

    df2['family_size'] = df2['SibSp'] + df2['Parch'] + 1

    grouped = df2.groupby(['family_size', 'Pclass'], observed=True)
    summary = grouped['Fare'].agg(
        n_passengers='count',
        avg_fare='mean',
        min_fare='min',
        max_fare='max'
    ).reset_index()

    # Order by Pclass then family_size
    summary['Pclass'] = pd.Categorical(summary['Pclass'], categories=sorted(df2['Pclass'].unique()), ordered=True)
    summary = summary.sort_values(['Pclass', 'family_size']).reset_index(drop=True)
    return summary


def last_names(df: Optional[pd.DataFrame] = None) -> pd.Series:
    """
    Exercise 2 (part): Extract last names from Name column and return a frequency Series
    (index = last name, value = count), sorted descending.
    Name format in Titanic dataset is usually "Last, Title. Given".
    """
    if df is None:
        df = load_titanic()
    # Drop NAs first
    names = df['Name'].dropna().astype(str)
    # Extract last name as text before the first comma
    last = names.apply(lambda s: s.split(',')[0].strip())
    counts = last.value_counts()
    return counts


def visualize_demographic(df: Optional[pd.DataFrame] = None) -> 'plotly.graph_objs._figure.Figure':
    """
    Create a plot that directly answers the question:
      "Did women in first class have a higher survival rate than men in other classes?"
    Implementation: bar chart of survival_rate by AgeGroup, colored by Sex, faceted by Pclass.
    """
    if df is None:
        df = load_titanic()
    summary = survival_demographics(df)

    # Convert survival_rate to percentage for easier reading in tooltip/axis (optional)
    summary = summary.copy()
    summary['survival_rate_pct'] = summary['survival_rate'] * 100

    fig = px.bar(
        summary,
        x='AgeGroup',
        y='survival_rate_pct',
        color='Sex',
        barmode='group',
        facet_col='Pclass',
        category_orders={'AgeGroup': ['Child', 'Teen', 'Adult', 'Senior', 'Unknown']},
        labels={'survival_rate_pct': 'Survival rate (%)'},
        title='Survival rate by Age Group, Sex, and Passenger Class'
    )

    fig.update_yaxes(range=[0, 100])  # 0-100%
    fig.update_layout(legend_title_text='Sex', uniformtext_minsize=8)
    return fig


def visualize_families(df: Optional[pd.DataFrame] = None) -> 'plotly.graph_objs._figure.Figure':
    """
    Create a plot to address: "How does average ticket fare vary with family size across classes?"
    Implementation: line plot of avg_fare vs family_size with one line per Pclass.
    """
    if df is None:
        df = load_titanic()
    summary = family_groups(df)

    # Ensure family_size is numeric (it should be)
    summary = summary.copy()
    summary['family_size'] = summary['family_size'].astype(int)

    fig = px.line(
        summary,
        x='family_size',
        y='avg_fare',
        color='Pclass',
        markers=True,
        labels={'family_size': 'Family size', 'avg_fare': 'Average fare'},
        title='Average ticket fare by family size and passenger class'
    )
    fig.update_xaxes(dtick=1)
    return fig


def visualize_family_size(df: Optional[pd.DataFrame] = None) -> 'plotly.graph_objs._figure.Figure':
    """
    Optional: show survival rate vs family size (useful bonus).
    """
    if df is None:
        df = load_titanic()
    df2 = df.copy()
    df2['family_size'] = df2['SibSp'].fillna(0).astype(int) + df2['Parch'].fillna(0).astype(int) + 1
    grouped = df2.groupby('family_size', observed=True)['Survived'].agg(n_passengers='count', n_survivors='sum').reset_index()
    grouped['survival_rate'] = grouped['n_survivors'] / grouped['n_passengers']
    fig = px.bar(grouped, x='family_size', y='survival_rate', labels={'survival_rate': 'Survival rate (0-1)'}, title='Survival rate by family size')
    return fig
