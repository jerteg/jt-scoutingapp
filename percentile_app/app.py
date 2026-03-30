import os
import sys

# 🔥 eerst path fix
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

# 🔹 daarna imports
import streamlit as st
import pandas as pd 

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {
    background-color: #fff5f5;
}

[data-testid="stSidebar"] {
    background-color: #f9f1f1;
}

body {
    color: #222;
}
</style>
""",
unsafe_allow_html=True
)

from shared.templates import report_template, position_groups, position_category_weights
from shared.data_processing import preprocess_data

all_stats = []

for group in report_template.values():
    all_stats.extend(group["stats"])

# 🔹 data laden
data_path = os.path.join(BASE_DIR, "shared", "data.csv")
data = pd.read_csv(data_path)

data = preprocess_data(data)



# 🔹 main position maken
data['Main Position'] = data['Position'].astype(str).str.split(',').str[0].str.strip()

def calculate_weighted_score(stats, weights, percentiles):
    total_weight = sum(weights.values())
    score = 0

    for stat in stats:
        if stat in percentiles and stat in weights:
            score += percentiles[stat] * weights[stat]

    return score / total_weight if total_weight > 0 else 0

def calculate_overall(category_scores, weights):
    total_weight = sum(weights.values())
    score = 0

    for cat, w in weights.items():
        score += category_scores.get(cat, 0) * w

    return score / total_weight if total_weight > 0 else 0

def get_color(value):
    if value >= 75:
        return "#1a9850"
    elif value >= 50:
        return "#91cf60"
    elif value >= 25:
        return "#fdae61"
    else:
        return "#d73027"

# =========================
# 🔹 SIDEBAR FILTERS
# =========================

with st.sidebar:

    st.title("JT Player Card")
    
    st.header("Filters")

    position_group = st.selectbox("Position Group", list(position_groups.keys()))
    positions = position_groups[position_group]

    countries = ["All"] + sorted(data['Birth country'].dropna().unique())
    country = st.selectbox("Birth country", countries)

    league_options = ["All"] + sorted(data['League'].dropna().unique())
    league = st.selectbox("League", league_options)

    min_age = int(data['Age'].min())
    max_age = int(data['Age'].max())

    age_range = st.slider("Age Range", min_age, max_age, (min_age, max_age))

    goalscoring_range = st.slider(
        "Goalscoring score",
        0, 100, (0, 100)
    )
    
    chancecreation_range = st.slider(
        "Chance creation score", 
        0, 100, (0, 100)
    )

    dribbling_range = st.slider(
        "Dribbling score", 
        0, 100, (0, 100)
    )

    passing_range = st.slider(
        "Passing score", 
        0, 100, (0, 100)
    )

    defending_range = st.slider(
        "Defending score", 
        0, 100, (0, 100)
    )

    all_stats = []

    for group in report_template.values():
        all_stats.extend(group["stats"])

# =========================
# 🔹 PERCENTILES (PER POSITION GROUP)
# =========================

percentile_data = data[data['Main Position'].isin(positions)].copy()

existing_stats = [stat for stat in all_stats if stat in percentile_data.columns]

percentiles = percentile_data[existing_stats].rank(pct=True) * 100

for category, group in report_template.items():

    stats = [s for s in group["stats"] if s in percentiles.columns]
    weights = group.get("weights", {})

    percentile_subset = percentiles[stats]

    percentile_data[f"{category}_score"] = percentile_subset.apply(
        lambda row: calculate_weighted_score(stats, weights, row),
        axis=1
    )

# =========================
# 🔹 FILTERING
# =========================

filtered_data = percentile_data.copy()

# country filter
if country != "All":
    filtered_data = filtered_data[
        filtered_data['Birth country'] == country
    ]

# league filter
if league != "All":
    filtered_data = filtered_data[
        filtered_data['League'] == league
    ]

# sliders
filtered_data = filtered_data[
    filtered_data['Age'].between(*age_range) &
    filtered_data['Goalscoring_score'].between(*goalscoring_range) &
    filtered_data['Chance creation_score'].between(*chancecreation_range) &
    filtered_data['Dribbling_score'].between(*dribbling_range) &
    filtered_data['Passing_score'].between(*passing_range) &
    filtered_data['Defending_score'].between(*defending_range)
]

# 🔹 check
if filtered_data.empty:
    st.warning("No players found with current filters")
    st.stop()

# 🔹 speler kiezen
players = sorted(filtered_data['Player'].unique())
player = st.sidebar.selectbox("Player", players)

player_data = filtered_data[filtered_data['Player'] == player].iloc[0]

category_scores = {
    category: player_data.get(f"{category}_score", 0)
    for category in report_template.keys()
}

weights = position_category_weights.get(position_group, {})
overall_score = calculate_overall(category_scores, weights)

team = player_data['Team within selected timeframe']

# =========================
# 🔹 HEADER (CORRECT)
# =========================
pos = player_data["Main Position"]
age = player_data["Age"]
league = player_data["League"]
minutes = player_data.get("Minutes played", "N/A")

color = get_color(overall_score)

html = f"""<div style="background:#f9f1f1; padding:12px 16px; border-radius:10px; margin-bottom:15px; display:flex; justify-content:space-between; align-items:center;">
    <div>
        <div style="font-size:30px;font-weight:800;">{player}</div>
        <div style="font-size:14px;color:#555;">
            {pos} | {team} | {age} yrs | {league} | {minutes} mins
        </div>
    </div>
    <div style="background:{color}; color:white; padding:10px 18px; font-size:20px; font-weight:800;">
        {overall_score:.0f}
    </div>
</div>"""

st.markdown(html, unsafe_allow_html=True)

# =========================
# 🔹 PERCENTILES
# =========================



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

def stat_bar(label, value, raw_value=None):

    # kleur
    if value >= 75:
        color = "#1a9850"
    elif value >= 50:
        color = "#91cf60"
    elif value >= 25:
        color = "#fdae61"
    else:
        color = "#d73027"

    # 🔹 detecteer per pass
    label_lower = label.lower()

    is_per_pass = "per pass" in label_lower
    is_per_received_pass = "per received pass" in label_lower

    if is_per_pass:
        label = label.replace(" per pass", "")
    elif is_per_received_pass:
        label = label.replace(" per received pass", "")

    display_raw = raw_value
    suffix = ""

    if (is_per_pass or is_per_received_pass) and raw_value is not None:
        try:
            display_raw = float(str(raw_value).replace(",", ".")) * 100

            if is_per_pass:
                suffix = " per 100 passes"
            elif is_per_received_pass:
                suffix = " per 100 received passes"

        except:
            display_raw = raw_value

    # 🔹 formatting (FIX voor komma probleem)
    if isinstance(display_raw, (int, float)):
        raw_text = f"{display_raw:.1f}".replace(",", ".") + suffix
    else:
        raw_text = str(display_raw).replace(",", ".")

    # 🔹 HTML
    st.markdown(
        f"""
        <div style="margin-bottom:10px">
            <div style="font-size:13px; color:#333">
                {label}
                <span style="float:right; color:#666">{raw_text}</span>
            </div>
            <div style="background:#eee; height:8px; border-radius:4px;">
                <div style="width:{value}%; background:{color}; height:8px; border-radius:4px;"></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================
# 🔹 SORTING (BESTE STATS BOVENAAN)
# =========================

for category, group in report_template.items():

    stats = [s for s in group["stats"] if s in player_percentiles.index]
    weights = group.get("weights", {})

    score = calculate_weighted_score(stats, weights, player_percentiles)

    color = get_color(score)

    st.markdown(
        f"""
        <div style="
            background:#f9f1f1;
            padding:12px 16px;
            margin-top:15px;
            margin-bottom:15px;
            display:flex;
            justify-content:space-between;
            align-items:center;
        ">
            <b>{category}</b>
            <span style="background:{color};color:white;padding:2px 10px;border-radius:10px;">
                {score:.0f}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )


    col1, col2 = st.columns(2)

    import math
    half = math.ceil(len(stats) / 2)

    with col1:
        for stat in stats[:half]:
            if stat in player_percentiles:
                value = player_percentiles[stat]
                raw_value = player_data[stat] if stat in player_data else None
                stat_bar(stat, value, raw_value)

    with col2:
        for stat in stats[half:]:
            if stat in player_percentiles:
                value = player_percentiles[stat]
                raw_value = player_data[stat] if stat in player_data else None
                stat_bar(stat, value, raw_value)

