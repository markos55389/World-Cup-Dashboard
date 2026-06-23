import streamlit as st
import pandas as pd
import random
import requests

# ----------------------------------------------------------------------
# 1. Page Configuration (MUST be first call, only once)
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
    df_init = pd.DataFrame(initial_data)
    df_init["gd"] = df_init["gf"] - df_init["ga"]
    df_init["points"] = df_init["won"] * 3 + df_init["drawn"]
    st.session_state.teams_df = df_init

if "current_page" not in st.session_state:
    st.session_state.current_page = "home"


def update_standings():
    df_temp = st.session_state.teams_df
    df_temp["gd"] = df_temp["gf"] - df_temp["ga"]
    df_temp["points"] = df_temp["won"] * 3 + df_temp["drawn"]
    st.session_state.teams_df = df_temp


# ----------------------------------------------------------------------
# 3. PAGE NAVIGATION ROUTER
# ----------------------------------------------------------------------

# --- PAGE 1: HOME ---
if st.session_state.current_page == "home":
    st.title("World Cup 2026")

    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        with st.container(border=True):
            st.subheader("Player Stats")
            st.write("View individual player performances and top scorers!")
            if st.button("Go to Player Stats ➔", type="primary", key="btn_p_stats"):
                st.session_state.current_page = "player_stats"
                st.rerun()
    with row1_col2:
        with st.container(border=True):
            st.subheader("Team Standings")
            st.write("View detailed group stage metrics and team ranks!")
            if st.button("Go to World Cup Standings ➔", type="primary", key="btn_t_stats"):
                st.session_state.current_page = "stats"
                st.rerun()

    st.markdown("---")
    with st.container(border=True):
        st.subheader("⚔️ Match Simulator")
        st.write("Predict match outcomes, run random simulations, and calculate updated table dynamics live!")
        if st.button("Launch Simulator Engine ➔", type="primary", key="btn_simulator_page"):
            st.session_state.current_page = "simulator"
            st.rerun()
    st.markdown("---")

    row2_col1, row2_col2 = st.columns(2)
    with row2_col1:
        with st.container(border=True):
            st.subheader("News")
            st.write("Get the latest updates about your favorite teams!")
            if st.button("Go to the latest news ➔", type="primary", key="btn_news"):
                st.session_state.current_page = "news"
                st.rerun()
    with row2_col2:
        with st.container(border=True):
            st.subheader("Competition")
            st.write("Track current tournament locations and standings!")
            if st.button("Find out where we are ➔", type="primary", key="btn_comp"):
                st.session_state.current_page = "competition"
                st.rerun()

# --- PAGE 2: TEAM STATS & STANDINGS ---
elif st.session_state.current_page == "stats":
    st.title("🏆 FIFA World Cup 2026 Standings")

    display_df = st.session_state.teams_df.copy()
    is_live = False

    # Comprehensive Flag Mapping Dictionary for World Cup Teams
    FLAG_MAP = {
        "Argentina": "🇦🇷", "Australia": "🇦🇺", "Austria": "🇦🇹", "Belgium": "🇧🇪",
        "Brazil": "🇧🇷", "Cameroon": "🇨🇲", "Canada": "🇨🇦", "Chile": "🇨🇱",
        "Colombia": "🇨🇴", "Costa Rica": "🇨🇷", "Croatia": "🇭🇷", "Denmark": "🇩🇰",
        "Ecuador": "🇪🇨", "Egypt": "🇪🇬", "England": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "France": "🇫🇷",
        "Germany": "🇩🇪", "Ghana": "🇬🇭", "Iran": "🇮🇷", "Italy": "🇮🇹",
        "Japan": "🇯🇵", "Mexico": "🇲🇽", "Morocco": "🇲🇦", "Netherlands": "🇳🇱",
        "Peru": "🇵🇪", "Poland": "🇵🇱", "Portugal": "🇵🇹", "Qatar": "🇶🇦",
        "Saudi Arabia": "🇸🇦", "Senegal": "🇸🇳", "Serbia": "🇷🇸", "South Korea": "🇰🇷",
        "Spain": "🇪🇸", "Sweden": "🇸🇪", "Switzerland": "🇨🇭", "Tunisia": "🇹🇳",
        "USA": "🇺🇸", "United States": "🇺🇸", "Uruguay": "🇺🇾", "Wales": "🏴󠁧󠁢󠁷󠁬󠁳󠁿"
    }

    # Browser imitation headers to prevent standard API blocks
    headers = {
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        # Load structural team metadata details
        teams_resp = requests.get("https://worldcup26.ir/get/teams", headers=headers, timeout=8)
        groups_resp = requests.get("https://worldcup26.ir/get/groups", headers=headers, timeout=8)

        if teams_resp.status_code == 200 and groups_resp.status_code == 200:
            teams_payload = teams_resp.json()
            groups_payload = groups_resp.json()

            # Normalize structural wrapper definitions from the JSON endpoints
            teams_list = teams_payload.get("data", teams_payload) if isinstance(teams_payload, dict) else teams_payload
            groups_list = groups_payload.get("data", groups_payload) if isinstance(groups_payload,
                                                                                   dict) else groups_payload

            # Build metadata lookup map
            meta_lookup = {}
            if isinstance(teams_list, list):
                for t in teams_list:
                    if isinstance(t, dict):
                        tid = str(t.get("id") or t.get("team_id") or "")
                        meta_lookup[tid] = {
                            "name": t.get("name_en") or t.get("name") or "Unknown Team",
                            "flag": t.get("flag") or t.get("emoji") or FLAG_MAP.get(t.get("name_en"), "⚽")
                        }

            all_teams = []
            if isinstance(groups_list, list):
                for group_obj in groups_list:
                    if isinstance(group_obj, dict):
                        group_letter = group_obj.get("group") or group_obj.get("name") or "G"
                        teams_array = group_obj.get("teams", [])

                        for idx, item in enumerate(teams_array):
                            if isinstance(item, dict):
                                target_id = str(item.get("team_id") or item.get("id") or "")
                                meta = meta_lookup.get(target_id, {"name": f"Team {target_id}", "flag": "⚽"})

                                # Read API values directly
                                points = int(item.get("pts") or item.get("points") or 0)
                                gf = int(item.get("gf") or item.get("goals_for") or 0)
                                ga = int(item.get("ga") or item.get("goals_against") or 0)

                                # Calculate missing variables directly from available metrics
                                won = points // 3
                                drawn = points % 3
                                played = int(item.get("played") or (won + drawn))
                                lost = max(0, played - (won + drawn))

                                all_teams.append({
                                    "name": meta["name"],
                                    "group": group_letter,
                                    "played": played,
                                    "won": won,
                                    "drawn": drawn,
                                    "lost": lost,
                                    "gf": gf,
                                    "ga": ga,
                                    "gd": gf - ga,
                                    "points": points,
                                    "flag": meta["flag"]
                                })

            if all_teams:
                display_df = pd.DataFrame(all_teams)
                is_live = True

    except Exception as api_err:
        pass  # Silently defaults to session state data if the local networking drops

    # Top KPI Cards
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Registered Teams", len(display_df))
    kpi2.metric("Total Goals Scored", int(display_df["gf"].sum()))
    kpi3.metric("Aggregated Matches", int(display_df["played"].sum()))
    kpi4.metric("Avg Points Per Team", round(display_df["points"].mean(), 1) if len(display_df) > 0 else 0)

    st.divider()
    if is_live:
        st.subheader("🔴 Live Group Stage Standings (Fetched from API)")
    else:
        st.subheader("📋 Group Stage Standings Table (Offline Backup)")

    # Sort rankings safely
    standings = display_df.sort_values(by=["points", "gd", "gf"], ascending=[False, False, False]).reset_index(
        drop=True)
    standings.insert(0, "Pos", range(1, len(standings) + 1))

    st.dataframe(
        standings[["Pos", "flag", "name", "group", "played", "won", "drawn", "lost", "gf", "ga", "gd", "points"]],
        column_config={
            "Pos": st.column_config.NumberColumn("Pos", width="small"),
            "flag": st.column_config.TextColumn("Flag", width="small"),
            "name": st.column_config.TextColumn("Team"),
            "group": st.column_config.TextColumn("Group"),
        },
        hide_index=True,
        use_container_width=True,
        height=400
    )

    st.divider()
    b1, b2 = st.columns(2)
    with b1:
        if st.button("⬅ Back to Home", key="back_home_from_stats", use_container_width=True):
            st.session_state.current_page = "home"
            st.rerun()
    with b2:
        if st.button("🔍 Team Deep Dive Explorer", key="go_to_explorer_from_stats", use_container_width=True):
            st.session_state.current_page = "🔍Explorer"
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