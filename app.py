import pandas as pd
import streamlit as st
import duckdb

st.write("""
# SQL SRS 
Spaced Repetition System SQL practice
""")

option = st.selectbox(
    "What would you like to review?",
    ("Joins", "GroupBy", "Windows Functions"),
    index=None,
    placeholder="Select a theme...", )

st.write('You selected', option)

data = {"a": [1, 2, 3], "b": [4, 5, 6]}
df = pd.DataFrame(data)
st.dataframe(df)
input_text = st.text_area(label="entrer votre input")

if input_text != "":
    st.write(f"Vous avez entrer la requête suivante: {input_text}")
    st.write("Voici le resultat de votre requête:")
    query = duckdb.sql(input_text).df()
    st.dataframe(query)


