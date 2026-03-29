import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

import streamlit as st
import pandas as pd

from radar_app.radar import create_radar
from shared.templates import template_config
from shared.data_processing import preprocess_data

# 🔹 titel
st.title("JT Radar Tool")
st.markdown("---")
st.markdown("### Filters")

# 🔹 data laden
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
data_path = os.path.join(BASE_DIR, "shared", "data.csv")

data = pd.read_csv(data_path)

# 🔹 preprocessing (HEEL BELANGRIJK)
data = preprocess_data(data)

# 🔹 template kiezen
template = st.selectbox(
    "Template",
    list(template_config.keys())
)

# 🔹 config ophalen
config = template_config[template]
positions = config["positions"]

# 🔹 main position maken
data['Main Position'] = data['Position'].astype(str).str.split(',').str[0].str.strip()

# 🔹 filter op positie
filtered_data = data[
    data['Main Position'].isin(positions)
]

# 🔹 league filter
league_options = ["All"] + sorted(filtered_data['League'].dropna().unique())
league = st.selectbox("League", league_options)

if league != "All":
    filtered_data = filtered_data[
        filtered_data['League'] == league
    ]

# 🔹 age filter
min_age = int(filtered_data['Age'].min())
max_age = int(filtered_data['Age'].max())

age_range = st.slider(
    "Age Range",
    min_age,
    max_age,
    (min_age, max_age)
)

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
player = st.selectbox("Search player", players)

# 🔹 team bepalen (BELANGRIJK bij duplicates)
team = filtered_data[
    filtered_data['Player'] == player
]['Team within selected timeframe'].iloc[0]

# 🔹 radar knop
if st.button("Generate Radar"):
    try:
        fig = create_radar(data, player, team, template)
        st.pyplot(fig)

    except IndexError:
        st.error("Error generating radar: player data incomplete")

    except Exception as e:
        st.error(f"Unexpected error: {e}")
