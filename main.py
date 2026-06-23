import streamlit as st
import pandas as pd
import random

# Load your World Cup data at the very top of the script
world_cup_data = {
    "flag": ["🇦🇷", "🇫🇷", "🇭🇷", "🇲🇦", "🇧🇷", "🇳🇱"],
    "name": ["Argentina", "France", "Croatia", "Morocco", "Brazil", "Netherlands"],
    "group": ["C", "D", "F", "F", "G", "A"],
    "played": [7, 7, 7, 7, 5, 5],
    "won": [4, 4, 2, 3, 3, 3],
    "drawn": [2, 1, 4, 2, 1, 2],
    "lost": [1, 2, 1, 2, 1, 0],
    "gf": [15, 16, 8, 6, 8, 10],
    "ga": [8, 7, 7, 5, 3, 4],
    "gd": [7, 9, 1, 1, 5, 6],
    "points": [14, 13, 10, 11, 10, 11]
}

df = pd.DataFrame(world_cup_data)
# ----------------------------------------------------------------------
# Page Configuration
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="FIFA World Cup 2026",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)
import streamlit as st

st.set_page_config(layout="wide")

# 1. Initialize the navigation state if it doesn't exist yet
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# --- PAGE 1: HOME (THE 4 BOXES) ---
if st.session_state.current_page == "home":
    st.title("Streamlit 4 Boxes Layout")

    # Row 1
    row1_col1, row1_col2 = st.columns(2)

    with row1_col1:
        with st.container(border=True):
            st.subheader("Box 1")
            st.write("Top Left Content")

    with row1_col2:
        with st.container(border=True):
            st.subheader("Team Stats")
            st.write("Click below to view the detailed statistics!")

            # Clicking this button changes the state to load the second view
            if st.button("Go to World Cup Stats ➔", type="primary"):
                st.session_state.current_page = "stats"
                st.rerun()

    # Row 2
    row2_col1, row2_col2 = st.columns(2)

    with row2_col1:
        with st.container(border=True):
            st.subheader("Box 3")
            st.write("Bottom Left Content")

    with row2_col2:
        with st.container(border=True):
            st.subheader("Box 4")
            st.write("Bottom Right Content")

# --- PAGE 2: DIFFERENT PART OF THE PROGRAM ---
elif st.session_state.current_page == "stats":
    st.subheader("Group Stage Standings")

    # Prepare standings table
    standings = df.sort_values(
        by=["points", "gd", "gf"],
        ascending=[False, False, False]
    ).reset_index(drop=True)
    standings.insert(0, "Pos", range(1, len(standings) + 1))

    # Display as nice dataframe
    st.dataframe(
        standings[["Pos", "flag", "name", "group", "played", "won", "drawn", "lost", "gf", "ga", "gd", "points"]],
        column_config={
            "Pos": st.column_config.NumberColumn("Pos", width="small"),
            "flag": st.column_config.TextColumn(""),
            "name": st.column_config.TextColumn("Team", width="medium"),
            "group": st.column_config.TextColumn("Group", width="small"),
            "gd": st.column_config.NumberColumn("GD", help="Goal Difference"),
            "points": st.column_config.NumberColumn("Pts", help="Points"),
        },
        hide_index=True,
        use_container_width=True,
        height=500
    )

    # A button to head back to the home layout
    if st.button("🔍 Team Explorer", key="go_to_explorer_from_stats"):
        st.session_state.current_page = "🔍Explorer"
        st.rerun()

# --- PAGE 3: DIFFERENT PART OF THE PROGRAM ---
elif st.session_state.current_page == "🔍Explorer":
         st.subheader("Team Deep Dive")

    if not df.empty:
             team_names = df["name"].tolist()
             selected_team = st.selectbox("Select a team", team_names, index=0)

             team = df[df["name"] == selected_team].iloc[0]

             # Header
             st.markdown(f"## {team['flag']} {team['name']} — Group {team['group']}")

             # Metrics
             m1, m2, m3, m4, m5 = st.columns(5)
             m1.metric("Points", int(team["points"]))
             m2.metric("Goal Difference", int(team["gd"]))
             m3.metric("Goals Scored", int(team["gf"]))
             m4.metric("Goals Conceded", int(team["ga"]))
             m5.metric("Matches Played", int(team["played"]))

             # W/D/L breakdown
             st.markdown("### Record")
             w, d, l = st.columns(3)
             w.metric("Wins", int(team["won"]))
             d.metric("Draws", int(team["drawn"]))
             l.metric("Losses", int(team["lost"]))

             # Simple bar chart
             chart_data = pd.DataFrame({
                 "Category": ["Goals Scored", "Goals Conceded"],
                 "Goals": [team["gf"], team["ga"]]
             })
             st.bar_chart(chart_data.set_index("Category"), use_container_width=True)
    else:
             st.warning("No teams match your filters.")
    if st.button("⬅ Back to Home", key="back_home_from_explorer"):
        st.session_state.current_page = "home"
        st.rerun()
    if st.button("🏆 Standings", key="go_to_standings_from_explorer"):
        st.session_state.current_page = "stats"
        st.rerun()
# ----------------------------------------------------------------------
# Session State Initialization
# ----------------------------------------------------------------------
if "teams_df" not in st.session_state:
    initial_data = [
        {"name": "Brazil", "flag": "🇧🇷", "group": "A", "played": 3, "won": 2, "drawn": 1, "lost": 0, "gf": 8, "ga": 3},
        {"name": "France", "flag": "🇫🇷", "group": "B", "played": 3, "won": 2, "drawn": 0, "lost": 1, "gf": 7, "ga": 4},
        {"name": "Argentina", "flag": "🇦🇷", "group": "C", "played": 3, "won": 3, "drawn": 0, "lost": 0, "gf": 9,
         "ga": 2},
        {"name": "England", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "group": "D", "played": 3, "won": 2, "drawn": 1, "lost": 0, "gf": 6,
         "ga": 2},
        {"name": "Spain", "flag": "🇪🇸", "group": "E", "played": 3, "won": 1, "drawn": 2, "lost": 0, "gf": 5, "ga": 3},
        {"name": "Germany", "flag": "🇩🇪", "group": "A", "played": 3, "won": 1, "drawn": 1, "lost": 1, "gf": 5, "ga": 4},
        {"name": "Portugal", "flag": "🇵🇹", "group": "B", "played": 3, "won": 2, "drawn": 0, "lost": 1, "gf": 6,
         "ga": 3},
        {"name": "Netherlands", "flag": "🇳🇱", "group": "C", "played": 3, "won": 1, "drawn": 1, "lost": 1, "gf": 4,
         "ga": 4},
    ]
    df = pd.DataFrame(initial_data)
    df["gd"] = df["gf"] - df["ga"]
    df["points"] = df["won"] * 3 + df["drawn"]
    st.session_state.teams_df = df


def update_standings():
    """Recalculate GD and Points"""
    df = st.session_state.teams_df
    df["gd"] = df["gf"] - df["ga"]
    df["points"] = df["won"] * 3 + df["drawn"]
    st.session_state.teams_df = df


# ----------------------------------------------------------------------
# Sidebar
# ----------------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ Controls")

    # Group Filter
    groups = sorted(st.session_state.teams_df["group"].unique())
    selected_groups = st.multiselect(
        "Filter by Group",
        groups,
        default=groups
    )

    # Search
    search_term = st.text_input("🔍 Search Team", placeholder="Type team name...")

    st.divider()

    # Add New Team
    with st.expander("➕ Add New Team", expanded=False):
        with st.form("add_team_form"):
            new_name = st.text_input("Team Name")
            new_flag = st.text_input("Flag Emoji", value="🏳️")
            new_group = st.selectbox("Group", ["A", "B", "C", "D", "E", "F", "G", "H"])

            col1, col2 = st.columns(2)
            with col1:
                new_played = st.number_input("Matches Played", 0, 10, 0)
                new_won = st.number_input("Won", 0, 10, 0)
                new_drawn = st.number_input("Drawn", 0, 10, 0)
            with col2:
                new_lost = st.number_input("Lost", 0, 10, 0)
                new_gf = st.number_input("Goals For", 0, 50, 0)
                new_ga = st.number_input("Goals Against", 0, 50, 0)

            submitted = st.form_submit_button("Add Team")
            if submitted and new_name:
                new_team = pd.DataFrame([{
                    "Name": new_name,
                    "Flag": new_flag,
                    "Group": new_group,
                    "Played": new_played,
                    "Won": new_won,
                    "Drawn": new_drawn,
                    "Lost": new_lost,
                    "GF": new_gf,
                    "GA": new_ga
                }])
                st.session_state.teams_df = pd.concat(
                    [st.session_state.teams_df, new_team], ignore_index=True
                )
                update_standings()
                st.success(f"{new_name} added successfully!")
                st.rerun()

    st.divider()

    if st.button("🔄 Reset All Data", type="secondary"):
        del st.session_state.teams_df
        st.rerun()

# ----------------------------------------------------------------------
# Main Content
# ----------------------------------------------------------------------
st.title("⚽ FIFA World Cup 2026")
st.caption("Interactive Group Stage Dashboard • Built with Streamlit")

# Filter dataframe
df = st.session_state.teams_df.copy()
if selected_groups:
    df = df[df["group"].isin(selected_groups)]
if search_term:
    df = df[df["name"].str.contains(search_term, case=False, na=False)]

# Top KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Teams", len(df))
col2.metric("Total Goals", int(df["gf"].sum()))
col3.metric("Matches Played", int(df["played"].sum()))
col4.metric("Avg Points", round(df["points"].mean(), 1))

st.divider()

# Tabs
tab1, tab2, tab3 = st.tabs(["🏆 Standings", "🔍 Team Explorer", "⚔️ Match Simulator"])

# ===================== TAB 1: STANDINGS =====================
with tab1:
    st.subheader("Group Stage Standings")

    # Prepare standings table
    standings = df.sort_values(
        by=["points", "gd", "gf"],
        ascending=[False, False, False]
    ).reset_index(drop=True)
    standings.insert(0, "Pos", range(1, len(standings) + 1))

    # Display as nice dataframe
    st.dataframe(
        standings[["Pos", "flag", "name", "group", "played", "won", "drawn", "lost", "gf", "ga", "gd", "points"]],
        column_config={
            "Pos": st.column_config.NumberColumn("Pos", width="small"),
            "flag": st.column_config.TextColumn(""),
            "name": st.column_config.TextColumn("Team", width="medium"),
            "group": st.column_config.TextColumn("Group", width="small"),
            "gd": st.column_config.NumberColumn("GD", help="Goal Difference"),
            "points": st.column_config.NumberColumn("Pts", help="Points"),
        },
        hide_index=True,
        use_container_width=True,
        height=500
    )

# ===================== TAB 2: TEAM EXPLORER =====================
with tab2:
    st.subheader("Team Deep Dive")

    if not df.empty:
        team_names = df["name"].tolist()
        selected_team = st.selectbox("Select a team", team_names, index=0)

        team = df[df["name"] == selected_team].iloc[0]

        # Header
        st.markdown(f"## {team['flag']} {team['name']} — Group {team['group']}")

        # Metrics
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Points", int(team["points"]))
        m2.metric("Goal Difference", int(team["gd"]))
        m3.metric("Goals Scored", int(team["gf"]))
        m4.metric("Goals Conceded", int(team["ga"]))
        m5.metric("Matches Played", int(team["played"]))

        # W/D/L breakdown
        st.markdown("### Record")
        w, d, l = st.columns(3)
        w.metric("Wins", int(team["won"]))
        d.metric("Draws", int(team["drawn"]))
        l.metric("Losses", int(team["lost"]))

        # Simple bar chart
        chart_data = pd.DataFrame({
            "Category": ["Goals Scored", "Goals Conceded"],
            "Goals": [team["gf"], team["ga"]]
        })
        st.bar_chart(chart_data.set_index("Category"), use_container_width=True)
    else:
        st.warning("No teams match your filters.")

# ===================== TAB 3: MATCH SIMULATOR =====================
with tab3:
    st.subheader("Match Simulator")
    st.caption("Simulate results and watch the standings update live")

    col1, col2 = st.columns(2)

    with col1:
        home_team = st.selectbox("Home Team", df["name"].tolist(), key="home")
    with col2:
        away_team = st.selectbox("Away Team", df["name"].tolist(), key="away", index=1)

    if home_team == away_team:
        st.warning("Please select two different teams.")
    else:
        sim_col1, sim_col2 = st.columns([1, 1])

        with sim_col1:
            if st.button("🎲 Simulate Random Result", use_container_width=True):
                home_goals = random.randint(0, 4)
                away_goals = random.randint(0, 4)
                st.session_state.sim_result = (home_goals, away_goals)

        with sim_col2:
            with st.form("manual_result"):
                h_goals = st.number_input("Home Goals", 0, 10, 2)
                a_goals = st.number_input("Away Goals", 0, 10, 1)
                submit = st.form_submit_button("Submit Result", use_container_width=True)

                if submit:
                    st.session_state.sim_result = (h_goals, a_goals)

        # Process simulation
        if "sim_result" in st.session_state:
            hg, ag = st.session_state.sim_result

            # Update stats
            teams_df = st.session_state.teams_df

            # Home team
            home_mask = teams_df["name"] == home_team
            teams_df.loc[home_mask, "played"] += 1
            teams_df.loc[home_mask, "gf"] += hg
            teams_df.loc[home_mask, "ga"] += ag

            # Away team
            away_mask = teams_df["name"] == away_team
            teams_df.loc[away_mask, "played"] += 1
            teams_df.loc[away_mask, "gf"] += ag
            teams_df.loc[away_mask, "ga"] += hg

            # Determine result
            if hg > ag:
                teams_df.loc[home_mask, "won"] += 1
                teams_df.loc[away_mask, "lost"] += 1
                result_text = f"**{home_team}** wins!"
            elif ag > hg:
                teams_df.loc[away_mask, "won"] += 1
                teams_df.loc[home_mask, "lost"] += 1
                result_text = f"**{away_team}** wins!"
            else:
                teams_df.loc[home_mask, "drawn"] += 1
                teams_df.loc[away_mask, "drawn"] += 1
                result_text = "It's a **draw**!"

            update_standings()

            # Show result
            st.success(f"### {home_team} {hg} - {ag} {away_team}")
            st.markdown(result_text)

            # Clear result after showing
            del st.session_state.sim_result
            st.rerun()

# Footer
st.divider()
st.caption("Built with ❤️ using Streamlit • Data updates in real-time")