import streamlit as st
from apputil import *

# Load Titanic dataset (you already do this)
df = pd.read_csv('https://raw.githubusercontent.com/leontoddjohnson/datasets/main/data/titanic.csv')

st.write("# Titanic Visualization 1")
st.write("**Question:** Did women in first class have a higher survival rate than men in other classes?")

fig1 = visualize_demographic(df)
st.plotly_chart(fig1, use_container_width=True)


st.write("# Titanic Visualization 2")
st.write("**Question:** How does average ticket fare vary with family size across passenger classes?")

fig2 = visualize_families(df)
st.plotly_chart(fig2, use_container_width=True)


st.write("# Titanic Visualization Bonus")
st.write("**Question (bonus):** How does survival rate change with family size?")

fig3 = visualize_family_size(df)
st.plotly_chart(fig3, use_container_width=True)

