import os
import sys

# 🔥 eerst path fix
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

# 🔹 daarna imports
import streamlit as st
import pandas as pd 

from shared.templates import report_template, position_groups
from shared.data_processing import preprocess_data

# 🔹 data laden
data_path = os.path.join(BASE_DIR, "shared", "data.csv")
data = pd.read_csv(data_path)

data = preprocess_data(data)

st.title("Player Report")

# 🔹 main position maken
data['Main Position'] = data['Position'].astype(str).str.split(',').str[0].str.strip()

# =========================
# 🔹 SIDEBAR FILTERS
# =========================

with st.sidebar:

    st.header("Filters")

    position_group = st.selectbox("Position Group", list(position_groups.keys()))
    positions = position_groups[position_group]

    league_options = ["All"] + sorted(data['League'].dropna().unique())
    league = st.selectbox("League", league_options)

    min_age = int(data['Age'].min())
    max_age = int(data['Age'].max())

    age_range = st.slider("Age Range", min_age, max_age, (min_age, max_age))

    all_stats = []

    for group in report_template.values():
        all_stats.extend(group["stats"])

# =========================
# 🔹 FILTERING
# =========================

filtered_data = data[data['Main Position'].isin(positions)]

if league != "All":
    filtered_data = filtered_data[filtered_data['League'] == league]

filtered_data = filtered_data[
    (filtered_data['Age'] >= age_range[0]) &
    (filtered_data['Age'] <= age_range[1])
]

# 🔹 check
if filtered_data.empty:
    st.warning("No players found with current filters")
    st.stop()

# 🔹 speler kiezen
players = sorted(filtered_data['Player'].unique())
player = st.sidebar.selectbox("Player", players)

player_data = filtered_data[filtered_data['Player'] == player].iloc[0]

team = player_data['Team within selected timeframe']

# =========================
# 🔹 HEADER
# =========================

st.markdown(f"## {player}")
st.markdown(
    f"{player_data['Team within selected timeframe']} | "
    f"{player_data['Age']} | "
    f"{player_data['Position']}"
)

st.markdown("---")

# =========================
# 🔹 PERCENTILES
# =========================

percentile_data = data[
    data['Main Position'].isin(positions)
]

existing_stats = [stat for stat in all_stats if stat in percentile_data.columns]
percentiles = percentile_data[existing_stats].rank(pct=True) * 100

player_percentiles = percentiles[
    (percentile_data['Player'] == player) &
    (percentile_data['Team within selected timeframe'] == team)
].iloc[0]

negative_stats = []

for stat in negative_stats:
    if stat in player_percentiles:
        player_percentiles[stat] = 100 - player_percentiles[stat]
        
for group in report_template.values():
    negative_stats.extend(group.get("negative_stats", []))

# =========================
# 🔹 STAT BAR FUNCTIE
# =========================

def stat_bar(label, value):

    # kleur op basis van percentile
    if value >= 75:
        color = "#1a9850"
    elif value >= 50:
        color = "#91cf60"
    elif value >= 25:
        color = "#fdae61"
    else:
        color = "#d73027"

    clean_label = label.replace(" per 90", "").replace(" per pass", "")

    st.markdown(f"""
    <div style="margin-bottom:10px">
        <div style="font-size:13px; color:#333">{clean_label}</div>
        <div style="background:#eee; height:8px; border-radius:4px;">
            <div style="
                width:{value}%;
                background:{color};
                height:8px;
                border-radius:4px;">
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# =========================
# 🔹 SORTING (BESTE STATS BOVENAAN)
# =========================


for category, group in report_template.items():
    stats = group["stats"]

    st.markdown(f"### {category}")

    col1, col2 = st.columns(2)

    half = len(stats) // 2

    with col1:
        for stat in stats[:half]:
            if stat in player_percentiles:
                value = player_percentiles[stat]
                stat_bar(stat, value)

    with col2:
        for stat in stats[half:]:
            if stat in player_percentiles:
                value = player_percentiles[stat]
                stat_bar(stat, value)

st.markdown("---")