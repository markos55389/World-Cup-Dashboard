import streamlit as st


class Team:
    def __init__(self, name, scored, against):
        self.name = name
        self.scored = scored
        self.against = against

    def goal_difference(self):
        return self.scored - self.against

st.title("⚽ World Cup Dashboard")
st.write("Welcome to my first Streamlit app!")

st.header("Brazil")

col1, col2, col3 = st.columns(3)
col1.metric("Scored", 9)
col2.metric("Conceded", 2)
col3.metric("Goal Difference", 7)

team = st.selectbox(
    "Pick a team",
    ["Brazil", "France", "Argentina", "England"]
)
st.write("You picked:", team)

#goals = st.slider("Goals scored", 0, 20, 0)
#st.write(team, "scored", goals, "goals")

teams = [
    Team("Brazil", 9, 2),
    Team("France", 7, 3),
    Team("Argentina", 8, 4),
    Team("England", 6, 2),
]

for t in teams:
    st.write(t.name, "— GD:", t.goal_difference())

if st.button("Celebrate"):
    st.balloons()



