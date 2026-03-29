import os
import sys

# 🔥 eerst path fix
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

import streamlit as st
import pandas as pd

from shared.data_processing import preprocess_data
from ranking import calculate_zscores, scale_zscores, apply_score_filters, calculate_rating
from shared.templates import template_config, position_groups, position_to_template

st.set_page_config(layout="wide")

# =========================================================
# 🔹 DATA
# =========================================================

data_path = os.path.join(BASE_DIR, "shared", "data.csv")
data = pd.read_csv(data_path)

data = preprocess_data(data)

# main position
data['Main Position'] = data['Position'].astype(str).str.split(',').str[0].str.strip()
from shared.templates import position_map
data['Position Label'] = data['Main Position'].map(position_map)
data['Position Label'] = data['Position Label'].fillna(data['Main Position'])

# =========================================================
# 🎯 SELECTIES
# =========================================================

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:
    st.title("JT Ranking Tool")

    st.markdown("---")

    # 🔹 Player filters
    st.markdown("### 🧍 Player")
    position_group = st.selectbox("Position", list(position_groups.keys()))

    age_range = st.slider("Age", 16, 40, (16, 40), step=1)
    value_range = st.slider("Market Value", 0, 20000000, (0, 20000000), step=50000)
    height_range = st.slider("Height", 150, 210, (150, 210), step=1)
    minutes_range = st.slider("Minutes played", 0, 10000, (0, 10000), step=100)

    foot = st.multiselect("Foot", ["left", "right", "both"])

    st.markdown("---")

    # 🔹 Stats selectie
    st.markdown("### 📊 Performance")
    template_name = position_to_template[position_group]
    template_stats = template_config[template_name]["stats"]

    stats = st.multiselect(
        "Select stats",
        template_stats,
        default=[]
    )

    if not stats:
        st.info("Select stats to generate ranking")
        st.stop()

    st.markdown("---")

    # 🔹 Stat filters
    st.markdown("### 🎚️ Stat filters")

    score_filters = {}
    for stat in stats:
        score_filters[stat] = st.slider(stat, 0, 100, (0, 100))

    st.markdown("### ⚖️ Weights")

    weights = {}

    default_weight = 1 / len(stats)

    for stat in stats:
        weights[stat] = st.slider(
            f"{stat} weight",
            0.0,
            1.0,
            default_weight
        )

    total_weight = sum(weights.values())

    if total_weight == 0:
        st.warning("Select at least one weight > 0")
        st.stop()

    normalized_weights = {
        stat: w / total_weight for stat, w in weights.items()
    }


# =========================================================
# 📌 POSITION DATA (BELANGRIJK)
# =========================================================

positions = position_groups[position_group]

position_data = data[
    data['Main Position'].isin(positions)
].copy()

# =========================================================
# 🔍 BASIS FILTERS
# =========================================================

filtered_data = position_data.copy()

filtered_data = filtered_data[
    (filtered_data['Age'] >= age_range[0]) &
    (filtered_data['Age'] <= age_range[1]) &
    (filtered_data['Market value'] >= value_range[0]) &
    (filtered_data['Market value'] <= value_range[1]) &
    (filtered_data['Height'] >= height_range[0]) &
    (filtered_data['Height'] <= height_range[1]) &
    (filtered_data['Minutes played'] >= minutes_range[0]) &
    (filtered_data['Minutes played'] <= minutes_range[1])
]

if foot:
    filtered_data = filtered_data[
        filtered_data['Foot'].isin(foot)
    ]

# =========================================================
# 🔥 Z-SCORES (op volledige positie)
# =========================================================

zscore_data = calculate_zscores(position_data, stats)
scored_data = scale_zscores(zscore_data, stats)

# =========================================================
# 🔍 FILTERS TOEVOEGEN
# =========================================================

filtered_scores = apply_score_filters(scored_data, stats, score_filters)

# 🔹 combineer met basis filters
final_df = filtered_scores[
    filtered_scores.set_index(['Player', 'Team within selected timeframe']).index.isin(
        filtered_data.set_index(['Player', 'Team within selected timeframe']).index
    )
]

# =========================================================
# 🏆 RANKING
# =========================================================

st.title(f"{position_group} Ranking")

ranking = calculate_rating(final_df, stats, normalized_weights)

if ranking.empty:
    st.warning("⚠️ No players found with current filters")
    st.caption("Try adjusting filters (minutes, age, stats, etc.)")
    st.stop()

ranking = ranking.sort_values("Rating", ascending=False).reset_index(drop=True)
ranking["Rank"] = ranking.index + 1

search = st.text_input("🔍 Search player")

if search:
    ranking = ranking[
        ranking["Player"].str.contains(search, case=False, na=False)
    ]

st.caption(f"{len(ranking)} players found")
    
st.caption("Rating based on selected stats and weights (z-scores-based)")

display = ranking[
    [
        'Rank',
        'Player',
        'Age',
        'Position Label',
        'Foot',
        'Team within selected timeframe',
        'League',
        'Contract expires',
        'Rating'
    ]
].head(30).round(1)

display = display.rename(columns={
    "Team within selected timeframe": "Team",
    "Contract expires": "Contract",
    "Position Label": "Position"
})

display["Rank"] = display["Rank"].astype(str)
display["Rating"] = display["Rating"].map(lambda x: f"{x:.1f}")
display["Age"] = display["Age"].astype(str)

st.dataframe(display, use_container_width=True, hide_index=True)


