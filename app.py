import pandas as pd
import streamlit as st
import duckdb

st.write("Hello world!")
data = {"a": [1, 2, 3], "b": [4, 5, 6]}
df = pd.DataFrame(data)
st.dataframe(df)
input_text = st.text_area(label="entrer votre input")

if input_text != "":
    st.write(f"Vous avez entrer la requête suivante: {input_text}")
    st.write("Voici le resultat de votre requête:")
    query = duckdb.sql(input_text).df()
    st.dataframe(query)


