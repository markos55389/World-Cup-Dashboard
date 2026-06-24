import streamlit as st
import pandas as pd
import random
import requests

# ----------------------------------------------------------------------
# 1. Page Configuration
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="FIFA World Cup 2026",
    page_icon="⚽",
    layout="wide"
)

# ----------------------------------------------------------------------
# 2. Session State Initialization
# ----------------------------------------------------------------------
if "teams_df" not in st.session_state:
    initial_data = [
        {"name": "Brazil", "flag": "🇧🇷", "group": "A", "played": 3, "won": 2, "drawn": 1, "lost": 0, "gf": 8, "ga": 3},
        {"name": "France", "flag": "🇫🇷", "group": "B", "played": 3, "won": 2, "drawn": 0, "lost": 1, "gf": 7, "ga": 4},
        {"name": "Argentina", "flag": "🇦🇷", "group": "C", "played": 3, "won": 3, "drawn": 0, "lost": 0, "gf": 9, "ga": 2},
        {"name": "England", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "group": "D", "played": 3, "won": 2, "drawn": 1, "lost": 0, "gf": 6, "ga": 2},
        {"name": "Spain", "flag": "🇪🇸", "group": "E", "played": 3, "won": 1, "drawn": 2, "lost": 0, "gf": 5, "ga": 3},
        {"name": "Germany", "flag": "🇩🇪", "group": "A", "played": 3, "won": 1, "drawn": 1, "lost": 1, "gf": 5, "ga": 4},
        {"name": "Portugal", "flag": "🇵🇹", "group": "B", "played": 3, "won": 2, "drawn": 0, "lost": 1, "gf": 6, "ga": 3},
        {"name": "Netherlands", "flag": "🇳🇱", "group": "C", "played": 3, "won": 1, "drawn": 1, "lost": 1, "gf": 4, "ga": 4},
    ]
    df_init = pd.DataFrame(initial_data)
    df_init["gd"] = df_init["gf"] - df_init["ga"]
    df_init["points"] = df_init["won"] * 3 + df_init["drawn"]
    st.session_state.teams_df = df_init

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"


def update_standings():
    df = st.session_state.teams_df
    df["gd"] = df["gf"] - df["ga"]
    df["points"] = df["won"] * 3 + df["drawn"]
    st.session_state.teams_df = df


# ----------------------------------------------------------------------
# 3. HOME PAGE
# ----------------------------------------------------------------------
if st.session_state.current_page == "home":
    st.title("World Cup 2026")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Team Stats"):
            st.session_state.current_page = "stats"
            st.rerun()

    with col2:
        if st.button("Match Simulator"):
            st.session_state.current_page = "simulator"
            st.rerun()


# ----------------------------------------------------------------------
# 4. STATS PAGE (FIXED API)
# ----------------------------------------------------------------------
elif st.session_state.current_page == "stats":
    st.title("🏆 Standings")

    display_df = st.session_state.teams_df.copy()
    is_live = False

    api_url = "https://worldcup26.ir/get/groups"
    headers = {"User-Agent": "Mozilla/5.0"}

    def normalize(team):
        return {
            "name": team.get("name_en") or team.get("name") or "Unknown",
            "played": int(team.get("mp") or team.get("played") or 0),
            "won": int(team.get("w") or team.get("wins") or 0),
            "drawn": int(team.get("d") or team.get("draws") or 0),
            "lost": int(team.get("l") or team.get("losses") or 0),
            "gf": int(team.get("gf") or 0),
            "ga": int(team.get("ga") or 0),
            "points": int(team.get("pts") or team.get("points") or 0),
            "group": team.get("group") or "?"
        }

    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        st.write("API Status:", response.status_code)

        if response.status_code == 200:
            data = response.json()

            groups = []
            if isinstance(data, list):
                groups = data
            elif isinstance(data, dict):
                groups = data.get("data") or data.get("groups") or data.get("response") or []

            all_teams = []

            for group in groups:
                if isinstance(group, dict):
                    group_name = group.get("group") or group.get("name") or "?"

                    teams = group.get("teams") or []
                    if isinstance(teams, dict):
                        teams = teams.values()

                    for t in teams:
                        if isinstance(t, dict):
                            nt = normalize(t)
                            nt["group"] = group_name
                            all_teams.append(nt)

            if all_teams:
                display_df = pd.DataFrame(all_teams)
                is_live = True
                st.success(f"Live API loaded: {len(all_teams)} teams")
            else:
                st.warning("API returned data but no teams parsed")

        else:
            st.error("API request failed")

    except Exception as e:
        st.error("API connection failed")
        st.exception(e)

    # ---------------- UI ----------------
    standings = display_df.sort_values(
        by=["points", "gf", "gd"],
        ascending=[False, False, False]
    )

    standings.insert(0, "Pos", range(1, len(standings) + 1))

    st.dataframe(standings)


    if st.button("Back"):
        st.session_state.current_page = "home"
        st.rerun()

# --- NEW PAGE: MATCH SIMULATOR SECTION ---
elif st.session_state.current_page == "simulator":
    st.title("⚔️ Tournament Match Simulator")
    st.caption("Simulate match outcomes and watch the global league standings update in real-time.")

    sc1, sc2 = st.columns(2)
    with sc1:
        home_team = st.selectbox("Home Team Selection", st.session_state.teams_df["name"].tolist(), key="home")
    with sc2:
        away_team = st.selectbox("Away Team Selection", st.session_state.teams_df["name"].tolist(), key="away", index=1)

    if home_team == away_team:
        st.warning("Please select two distinct teams to simulate a match.")
    else:
        sim1, sim2 = st.columns(2)
        with sim1:
            if st.button("🎲 Run Instant Random Simulation", use_container_width=True):
                st.session_state.sim_result = (random.randint(0, 4), random.randint(0, 4))
        with sim2:
            with st.form("manual_result"):
                h_goals = st.number_input("Home Team Score Line", 0, 10, 2)
                a_goals = st.number_input("Away Team Score Line", 0, 10, 1)
                if st.form_submit_button("Log Official Score Result", use_container_width=True):
                    st.session_state.sim_result = (h_goals, a_goals)

        if "sim_result" in st.session_state:
            hg, ag = st.session_state.sim_result
            t_df = st.session_state.teams_df

            hm = t_df["name"] == home_team
            am = t_df["name"] == away_team

            t_df.loc[hm, "played"] += 1;
            t_df.loc[hm, "gf"] += hg;
            t_df.loc[hm, "ga"] += ag
            t_df.loc[am, "played"] += 1;
            t_df.loc[am, "gf"] += ag;
            t_df.loc[am, "ga"] += hg

            if hg > ag:
                t_df.loc[hm, "won"] += 1;
                t_df.loc[am, "lost"] += 1
                res_txt = f"**{home_team}** secures the victory!"
            elif ag > hg:
                t_df.loc[am, "won"] += 1;
                t_df.loc[hm, "lost"] += 1
                res_txt = f"**{away_team}** secures the victory!"
            else:
                t_df.loc[hm, "drawn"] += 1;
                t_df.loc[am, "drawn"] += 1
                res_txt = "The match ends in a **draw**!"

            st.session_state.teams_df = t_df
            update_standings()
            st.success(f"### Finished: {home_team} {hg} - {ag} {away_team}")
            st.markdown(res_txt)
            del st.session_state.sim_result
            st.rerun()

    st.divider()
    if st.button("⬅ Back to Home Layout", key="back_home_from_sim", use_container_width=True):
        st.session_state.current_page = "home"
        st.rerun()

# --- PAGE 3: TEAM EXPLORER ---
elif st.session_state.current_page == "🔍Explorer":
    st.subheader("Team Deep Dive")
    df_explorer = st.session_state.teams_df
    if not df_explorer.empty:
        team_names = df_explorer["name"].tolist()
        selected_team = st.selectbox("Select a team", team_names, index=0)
        team = df_explorer[df_explorer["name"] == selected_team].iloc[0]

        st.markdown(f"## {team['flag']} {team['name']} — Group {team['group']}")
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Points", int(team["points"]))
        m2.metric("Goal Difference", int(team["gd"]))
        m3.metric("Goals Scored", int(team["gf"]))
        m4.metric("Goals Conceded", int(team["ga"]))
        m5.metric("Matches Played", int(team["played"]))

        st.bar_chart(pd.DataFrame({"Goals": [team["gf"], team["ga"]]}, index=["Scored", "Conceded"]))

    if st.button("⬅ Back to Home", key="back_home_from_explorer"):
        st.session_state.current_page = "home"
        st.rerun()

# --- PAGE 4: PLAYER STATS ---
elif st.session_state.current_page == "player_stats":
    st.subheader("⚽ Player Statistics")
    player_data = {
        "Player": ["Lionel Messi", "Kylian Mbappé", "Luka Modrić", "Neymar Jr"],
        "Team": ["Argentina", "France", "Croatia", "Brazil"],
        "Goals": [7, 8, 3, 2], "Assists": [3, 2, 1, 1]
    }
    st.dataframe(pd.DataFrame(player_data), use_container_width=True, hide_index=True)
    if st.button("⬅ Back to Home", key="back_home_from_players"):
        st.session_state.current_page = "home"
        st.rerun()

# --- PAGE 5: NEWS ---
elif st.session_state.current_page == "news":
    st.subheader("📰 Latest News")
    search_query = st.text_input("🔍 Search Team News", placeholder="Type team name...")
    if search_query.strip():
        clean_name = search_query.strip().replace(" ", "+")
        st.link_button(f"Read latest news for {search_query.strip()} ➔",
                       f"https://www.google.com/search?q={clean_name}+latest+football+news", type="primary")
    if st.button("⬅ Back to Home", key="back_home_from_news"):
        st.session_state.current_page = "home"
        st.rerun()

# --- PAGE 6: COMPETITION ---
elif st.session_state.current_page == "competition":
    st.subheader("⚽ Competition Whereabouts")
    comp_query = st.text_input("🔍 Search Team Standings", placeholder="Type team name...")
    if comp_query.strip():
        clean_comp = comp_query.strip().replace(" ", "+")
        st.link_button(f"Check {comp_query.strip()}'s Progress ➔",
                       f"https://www.google.com/search?q={clean_comp}+world+cup", type="primary")

    st.markdown("### 📅 Quick Schedules & Results")
    l1, l2 = st.columns(2)
    l1.link_button("📅 See Upcoming Games", "https://www.google.com/search?q=world+cup+upcoming+games+fixtures",
                   use_container_width=True)
    l2.link_button("⚽ See Latest Played Games", "https://www.google.com/search?q=world+cup+latest+played+games+results",
                   use_container_width=True)
    if st.button("⬅ Back to Home", key="back_home_from_competition"):
        st.session_state.current_page = "home"
        st.rerun()

# ----------------------------------------------------------------------
# 4. Global Structural Footer
# ----------------------------------------------------------------------
st.divider()
st.caption("Built with ❤️ using Streamlit • Data updates in real-time")