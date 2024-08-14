import duckdb

import streamlit as st
import ast

# solution_df = duckdb.sql(answer_str).df()

con = duckdb.connect(database="data/exercices_sql_tables.duckdb", read_only=False)

with st.sidebar:
    theme = st.selectbox(
        "What would you like to review?",
        ("cross_joins", "GroupBy", "windows_functions"),
        index=None,
        placeholder="Select a theme...",
    )
    st.write("You selected:", theme)

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()
    st.write(exercise)

st.header("enter your code:")
query = st.text_area(label="votre code SQL ici", key="user_input")
if query:
    st.write("Resulat :")
    result = con.execute(query).df()
    st.dataframe(result)
#
#     try:
#         columns = result[solution_df.columns]
#         result = columns
#         st.dataframe(result.compare(solution_df))
#     except KeyError as e:
#         st.write("Some columns are missing")
#
#     n_lines_difference = result.shape[0] - solution_df.shape[0]
#     if n_lines_difference != 0:
#         st.write(
#             f"result has a {n_lines_difference} lines differences with the solution_df"
#         )
#
tab2, tab3 = st.tabs(["Tables", "Solution"])
with tab2:

    exercise_table = ast.literal_eval(exercise.loc[0, "tables"])
    for table in exercise_table:
        st.write(f"Table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.write(df_table)
#
with tab3:
    exercise_name = exercise.loc[0, "exercises_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()
    st.write(answer)
