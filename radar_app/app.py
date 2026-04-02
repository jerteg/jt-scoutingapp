import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

import streamlit as st
import pandas as pd

from radar_app.radar import create_radar, create_comparison_radar
from shared.templates import template_config, TOP5_LEAGUES, NEXT14_LEAGUES, LEAGUE_DISPLAY_NAMES
from shared.data_processing import preprocess_data

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="JT Radar Tool",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Styling ───────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
        .stApp { background-color: #f5ede8; }
        section[data-testid="stSidebar"] { background-color: #fdf6f2; }

        h1, h2, h3 { color: #1a1a2e; }

        .stSelectbox label, .stSlider label, .stRadio label {
            color: #1a1a2e !important;
            font-weight: 600;
        }

        .stButton > button {
            background-color: #c0392b;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            padding: 0.5rem 1.5rem;
            transition: background-color 0.2s;
        }
        .stButton > button:hover {
            background-color: #a93226;
            color: white;
        }

        hr { border-color: #e0c8be; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Data ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    data_path = os.path.join(BASE_DIR, "shared", "data.csv")
    df = pd.read_csv(data_path)
    df = preprocess_data(df)
    df["Main Position"] = df["Position"].astype(str).str.split(",").str[0].str.strip()
    return df

data = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Filters")
    st.markdown("---")

    # Mode
    mode = st.radio("Mode", ["Single Radar", "Comparison"], horizontal=True)
    st.markdown("---")

    # League template
    st.markdown("**League template**")
    league_template = st.radio(
        "league_template_radio",
        ["Top 5 leagues", "Next 14 competitions", "Both"],
        label_visibility="collapsed",
    )

    # Percentile basis
    st.markdown("**Percentile basis**")
    if league_template == "Top 5 leagues":
        pct_options = ["T5 only", "Own league"]
    elif league_template == "Next 14 competitions":
        pct_options = ["Next 14 only", "Own league"]
    else:
        pct_options = ["T5 + Next 14", "T5 only", "Next 14 only", "Own league"]

    percentile_basis = st.radio(
        "pct_basis_radio",
        pct_options,
        label_visibility="collapsed",
    )
    st.markdown("---")

    # Position group
    position_group = st.selectbox("Position Group", list(template_config.keys()))
    positions = template_config[position_group]["positions"]

    # Filter pool on league template
    filtered = data[data["Main Position"].isin(positions)].copy()
    if league_template == "Top 5 leagues":
        filtered = filtered[filtered["League"].isin(TOP5_LEAGUES)]
    elif league_template == "Next 14 competitions":
        filtered = filtered[filtered["League"].isin(NEXT14_LEAGUES)]

    # League filter (UI only)
    all_leagues = sorted(filtered["League"].dropna().unique())
    display_options = {LEAGUE_DISPLAY_NAMES.get(l, l): l for l in all_leagues}
    selected_display = st.selectbox("League (filter)", ["All"] + list(display_options.keys()))
    if selected_display != "All":
        filtered = filtered[filtered["League"] == display_options[selected_display]]

    # Club filter (UI only)
    clubs = sorted(filtered["Team within selected timeframe"].dropna().unique())
    selected_club = st.selectbox("Club (filter)", ["All"] + clubs)
    if selected_club != "All":
        filtered = filtered[filtered["Team within selected timeframe"] == selected_club]

    # Age filter
    if not filtered.empty:
        min_age = int(filtered["Age"].min())
        max_age = int(filtered["Age"].max())

        if min_age == max_age:
            st.markdown(f"**Age** {min_age}")
            age_range = (min_age, max_age)
        else:
            age_range = st.slider("Age Range", min_age, max_age, (min_age, max_age))
            
        filtered = filtered[
            (filtered["Age"] >= age_range[0]) &
            (filtered["Age"] <= age_range[1])
        ]

    if filtered.empty:
        st.warning("No players found with the current filters.")
        st.stop()

    st.markdown("---")

    # Player 1
    st.markdown("**Player 1**")
    players = sorted(filtered["Player"].unique())
    player1 = st.selectbox("Search player", players, key="p1")
    team1 = filtered[filtered["Player"] == player1]["Team within selected timeframe"].iloc[0]
    st.caption(f"🏟️ {team1}")

    # Player 2 (comparison only)
    if mode == "Comparison":
        st.markdown("**Player 2**")
        player2 = st.selectbox("Search player", players, key="p2",
                                index=min(1, len(players) - 1))
        team2 = filtered[filtered["Player"] == player2]["Team within selected timeframe"].iloc[0]
        st.caption(f"🏟️ {team2}")

        st.markdown("**Comparison view**")
        comparison_mode = st.radio(
            "comp_mode_radio",
            ["Side by side", "Overlay"],
            label_visibility="collapsed",
        )

    st.markdown("---")
    generate = st.button("🎯 Generate Radar", use_container_width=True)

# ── Main ──────────────────────────────────────────────────────────────────────
st.markdown("# 📡 JT Radar Tool")
st.markdown("---")

if generate:
    try:
        if mode == "Single Radar":
            with st.spinner("Generating radar..."):
                fig = create_radar(
                    data,
                    player_name=player1,
                    player_team=team1,
                    template_key=position_group,
                    percentile_basis=percentile_basis,
                )
            st.pyplot(fig, use_container_width=True)

        else:
            cmode = "side_by_side" if comparison_mode == "Side by side" else "overlay"
            with st.spinner("Generating comparison..."):
                fig = create_comparison_radar(
                    data,
                    player1_name=player1, player1_team=team1,
                    player2_name=player2, player2_team=team2,
                    template_key=position_group,
                    percentile_basis=percentile_basis,
                    mode=cmode,
                )
            st.pyplot(fig, use_container_width=True)

    except ValueError as e:
        st.error(f"❌ {e}")
    except KeyError as e:
        st.error(f"❌ Stat not found in data: {e}")
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")

else:
    st.markdown(
        """
        <div style="
            background-color: #fdf6f2;
            border: 2px dashed #e0c8be;
            border-radius: 12px;
            padding: 3rem;
            text-align: center;
            color: #6b6b7b;
        ">
            <h3 style="color:#6b6b7b;">Set your filters and click <b>Generate Radar</b></h3>
            <p>Choose a position group, percentile basis, player and generate the radar chart.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
