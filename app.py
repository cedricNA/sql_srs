import os
import logging
import duckdb
from datetime import date, timedelta
import streamlit as st

if "data" not in os.listdir():
    print("creating folder data")
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")


if "exercices_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())


if "exercices_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())

con = duckdb.connect(database="data/exercices_sql_tables.duckdb", read_only=False)


def check_users_solution(user_query: str) -> None:
    """
    Exécute la requête SQL fournie par l'utilisateur
    et compare les résultats avec une solution de référence.

    Args:
        user_query (str): La requête SQL à exécuter
        sous forme de chaîne de caractères.

    Returns:
        None: Cette fonction n'a pas de valeur de retour.
        Elle affiche les résultats et les comparaisons directement
        dans l'interface utilisateur Streamlit.

    """
    st.write("Resulat :")
    result = con.execute(user_query).df()
    st.dataframe(result)

    try:
        columns = result[solution_df.columns]
        result = columns
        st.dataframe(result.compare(solution_df))
    except KeyError as e:
        st.write("Some columns are missing")
    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"result has a {n_lines_difference} lines differences with the solution_df"
        )


def get_exercice():
    """
    Récupère un exercice à réviser en fonction du thème
    sélectionné par l'utilisateur .
    """

    available_theme_df = con.execute("SELECT DISTINCT theme FROM memory_state").df()
    theme = st.selectbox(
        "What would you like to review?",
        available_theme_df["theme"].unique(),
        index=None,
        placeholder="Select a theme...",
    )
    if theme:
        st.write(f"You selected: {theme}")
        select_exercise_query = f"SELECT * FROM memory_state WHERE theme = '{theme}'"

    else:
        select_exercise_query = f"SELECT * FROM memory_state"
        st.write("Please choose a theme to begin")
    exercise_df = (
        con.execute(f"SELECT * FROM memory_state")
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop=True)
    )
    return exercise_df


with st.sidebar:

    exercise = get_exercice()
    st.write(exercise)

    exercise_name = exercise.loc[0, "exercises_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()


solution_df = con.execute(answer).df()

st.title("SRS Space Repetition System")
query = st.text_area(label="Your code here", key="user_input")


if query:
    check_users_solution(query)

n_days_list = [2, 7, 21]

cols = st.columns(len(n_days_list))

for i, n_days in enumerate(n_days_list):
    with cols[i]:
        if st.button(f"Revoir dans :{n_days} jours"):
            next_review = date.today() + timedelta(days=n_days)
            con.execute(
                f"UPDATE memory_state SET last_reviewed ='{next_review}' WHERE exercises_name= '{exercise_name}'"
            )
            st.rerun()

if st.button("Reset"):
    con.execute("UPDATE memory_state SET last_reviewed = '1970-01-01'")
    st.rerun()

tab2, tab3 = st.tabs(["Tables", "Solution"])
with tab2:

    exercise_table = exercise.loc[0, "tables"]
    for table in exercise_table:
        st.write(f"Table: {table}")
        df_table = con.execute(f"SELECT * FROM {table}").df()
        st.write(df_table)
#
with tab3:

    st.write(answer)
    st.write(solution_df)
