import os
import sys
import math
import base64
import io

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background-color: #fff5f5; }
[data-testid="stSidebar"]          { background-color: #f9f1f1; }
body                               { color: #222; }
</style>
""", unsafe_allow_html=True)

from shared.templates import report_template, position_groups, position_category_weights, LEAGUE_MULTIPLIERS_ALL, LEAGUE_MULTIPLIERS_NEXT14, TOP5_LEAGUES, NEXT14_LEAGUES
from shared.data_processing import preprocess_data

# ── Load & preprocess data ────────────────────────────────────────────────────
data_path = os.path.join(BASE_DIR, "shared", "data.csv")
data = pd.read_csv(data_path)
data = preprocess_data(data)
data['Main Position'] = data['Position'].astype(str).str.split(',').str[0].str.strip()

ALL_STATS = [s for group in report_template.values() for s in group["stats"]]

# ── Scoring helpers ───────────────────────────────────────────────────────────

def calculate_weighted_score(stats, weights, percentiles):
    total_weight = sum(weights.get(s, 0) for s in stats if s in percentiles)
    if total_weight == 0:
        return 0
    return sum(percentiles[s] * weights[s] for s in stats if s in percentiles and s in weights) / total_weight


def calculate_overall(category_scores, weights):
    total_weight = sum(weights.values())
    if total_weight == 0:
        return 0
    return sum(category_scores.get(cat, 0) * w for cat, w in weights.items()) / total_weight


def get_color(value):
    if value >= 75:
        return "#1a9850"
    elif value >= 50:
        return "#91cf60"
    elif value >= 25:
        return "#fdae61"
    return "#d73027"


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("JT Player Card")
    st.header("Filters")

    # League template (NEW)
    league_template = st.radio(
        "League template",
        options=["Top 5 leagues", "Next 14 competitions", "Both"],
        horizontal=True,
    )

    position_group = st.selectbox("Position Group", list(position_groups.keys()))
    positions = position_groups[position_group]

    score_mode = st.radio(
        "Score type",
        ["Model (raw)", "Adjusted (recommended)"]
    )

    countries = ["All"] + sorted(data['Birth country'].dropna().unique())
    country = st.selectbox("Birth country", countries)

    league_options = ["All"] + sorted(data['League'].dropna().unique())
    league_filter = st.selectbox("League", league_options)

    min_age, max_age = int(data['Age'].min()), int(data['Age'].max())
    age_range = st.slider("Age Range", min_age, max_age, (min_age, max_age))

    goalscoring_range    = st.slider("Goalscoring score",     0, 100, (0, 100))
    chancecreation_range = st.slider("Chance creation score", 0, 100, (0, 100))
    dribbling_range      = st.slider("Dribbling score",       0, 100, (0, 100))
    passing_range        = st.slider("Passing score",         0, 100, (0, 100))
    defending_range      = st.slider("Defending score",       0, 100, (0, 100))
    if score_mode == "Model (raw)":
        overall_label = "Overall score (model)"
    else:
        overall_label = "Overall score (adjusted)"

    overall_range = st.slider(overall_label, 0, 100, (0, 100))

# ── Filter pool for percentile reference ──────────────────────────────────────
if league_template == "Top 5 leagues":
    allowed_leagues = TOP5_LEAGUES
    multiplier_dict = LEAGUE_MULTIPLIERS_ALL  # belangrijk!

elif league_template == "Next 14 competitions":
    allowed_leagues = NEXT14_LEAGUES
    multiplier_dict = LEAGUE_MULTIPLIERS_NEXT14

else:
    allowed_leagues = set(LEAGUE_MULTIPLIERS_ALL.keys())
    multiplier_dict = LEAGUE_MULTIPLIERS_ALL

percentile_data = data[
    data['Main Position'].isin(positions) &
    data['League'].isin(allowed_leagues)
].copy()

existing_stats = [s for s in ALL_STATS if s in percentile_data.columns]

percentiles_raw = percentile_data[existing_stats].rank(pct=True) * 100

# ── Apply league-adjustment multiplier AFTER raw percentile ──────────────────
# Multiply each player's raw percentile by the league quality factor,
# then clip to [0, 100] so scores stay in range.
league_multipliers_series = (
    percentile_data['League']
    .map(multiplier_dict)
    .fillna(1.0)
)

percentiles = (
    percentiles_raw
    .multiply(league_multipliers_series.values, axis=0)
    .clip(0, 100)
)

# ── Category scores ───────────────────────────────────────────────────────────
for category, group in report_template.items():
    stats = [s for s in group["stats"] if s in percentiles.columns]
    weights = group.get("weights", {})
    negative_stats = group.get("negative_stats", [])

    def _score_row(row, stats=stats, weights=weights, negative_stats=negative_stats):
        adj = row.copy()
        for ns in negative_stats:
            if ns in adj:
                adj[ns] = 100 - adj[ns]
        return calculate_weighted_score(stats, weights, adj)

    percentile_data[f"{category}_score"] = percentiles[stats].apply(_score_row, axis=1)

    weights = position_category_weights.get(position_group, {})

    def _compute_overall(row):
        category_scores = {
            cat: row.get(f"{cat}_score", 0)
            for cat in report_template
        }
        return calculate_overall(category_scores, weights)

    percentile_data["overall_score"] = percentile_data.apply(_compute_overall, axis=1)

# ── Player-level filters ───────────────────────────────────────────────────────
filtered_data = percentile_data.copy()

if country != "All":
    filtered_data = filtered_data[filtered_data['Birth country'] == country]
if league_filter != "All":
    filtered_data = filtered_data[filtered_data['League'] == league_filter]

filtered_data = filtered_data[
    filtered_data['Age'].between(*age_range) &
    filtered_data['Goalscoring_score'].between(*goalscoring_range) &
    filtered_data['Chance creation_score'].between(*chancecreation_range) &
    filtered_data['Dribbling_score'].between(*dribbling_range) &
    filtered_data['Passing_score'].between(*passing_range) &
    filtered_data['Defending_score'].between(*defending_range)
]

if score_mode == "Model (raw)":
    overall_filter_scores = filtered_data["overall_score"]
else:
    overall_filter_scores = (filtered_data["overall_score"] / 100) ** 0.45 * 100

filtered_data = filtered_data[
    overall_filter_scores.between(*overall_range)
]

if filtered_data.empty:
    st.warning("No players found with current filters")
    st.stop()

if score_mode == "Model (raw)":
    scores_for_ranking = filtered_data["overall_score"]
else:
    scores_for_ranking = (filtered_data["overall_score"] / 100) ** 0.45 * 100

min_score = scores_for_ranking.min()
avg_score = scores_for_ranking.mean()
max_score = scores_for_ranking.max()

filtered_data["rank"] = scores_for_ranking.rank(method="first", ascending=False)

# ── Player selection ──────────────────────────────────────────────────────────
players = sorted(filtered_data['Player'].unique())
player = st.sidebar.selectbox("Player", players)

player_data = filtered_data[filtered_data['Player'] == player].iloc[0]
player_rank = int(player_data["rank"])
total_players = len(filtered_data)
team = player_data['Team within selected timeframe']

category_scores = {cat: player_data.get(f"{cat}_score", 0) for cat in report_template}
weights = position_category_weights.get(position_group, {})
overall_score = calculate_overall(category_scores, weights)
if score_mode == "Adjusted (recommended)":
    overall_score = (overall_score / 100) ** 0.45 * 100

pos     = player_data["Main Position"]
age     = player_data["Age"]
league  = player_data["League"]
minutes = player_data.get("Minutes played", "N/A")
color   = get_color(overall_score)

# ── Player percentile row ──────────────────────────────────────────────────────
player_percentiles = percentiles[
    (percentile_data['Player'] == player) &
    (percentile_data['Team within selected timeframe'] == team)
].iloc[0].copy()

# Invert negative stats
for group in report_template.values():
    for ns in group.get("negative_stats", []):
        if ns in player_percentiles:
            player_percentiles[ns] = 100 - player_percentiles[ns]

# ── Stat bar ───────────────────────────────────────────────────────────────────

def stat_bar(label, value, raw_value=None):
    bar_color = get_color(value)
    label_lower = label.lower()
    is_per_pass = "per pass" in label_lower and "received" not in label_lower
    is_per_recv = "per received pass" in label_lower

    if is_per_pass:
        label = label.replace(" per pass", "")
    elif is_per_recv:
        label = label.replace(" per received pass", "")

    suffix = ""
    display_raw = raw_value
    if (is_per_pass or is_per_recv) and raw_value is not None:
        try:
            display_raw = float(str(raw_value).replace(",", ".")) * 100
            suffix = " per 100 passes" if is_per_pass else " per 100 received passes"
        except (ValueError, TypeError):
            display_raw = raw_value

    if isinstance(display_raw, (int, float)):
        raw_text = f"{display_raw:.1f}" + suffix
    else:
        raw_text = str(display_raw).replace(",", ".")

    st.markdown(f"""
        <div style="margin-bottom:10px">
            <div style="font-size:13px;color:#333">
                {label}
                <span style="float:right;color:#666">{raw_text}</span>
            </div>
            <div style="background:#eee;height:8px;border-radius:4px;">
                <div style="width:{value:.1f}%;background:{bar_color};height:8px;border-radius:4px;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)


# ── Build card HTML (shared between display and PNG export) ───────────────────

def build_card_html(player, pos, team, age, league, minutes, overall_score,
                    category_scores, player_percentiles, player_data,
                    report_template, position_group, league_template):
    """Return a self-contained HTML string representing the player card."""

    def _color(v):
        if v >= 75: return "#1a9850"
        if v >= 50: return "#91cf60"
        if v >= 25: return "#fdae61"
        return "#d73027"

    def _bar(label, value, raw_value=None):
        lbl = label
        lbl_lower = label.lower()
        is_per_pass = "per pass" in lbl_lower and "received" not in lbl_lower
        is_per_recv = "per received pass" in lbl_lower
        if is_per_pass:
            lbl = lbl.replace(" per pass", "")
        elif is_per_recv:
            lbl = lbl.replace(" per received pass", "")

        suffix = ""
        display = raw_value
        if (is_per_pass or is_per_recv) and raw_value is not None:
            try:
                display = float(str(raw_value).replace(",", ".")) * 100
                suffix = " per 100 passes" if is_per_pass else " per 100 received passes"
            except (ValueError, TypeError):
                pass
        if isinstance(display, (int, float)):
            raw_text = f"{display:.1f}{suffix}"
        else:
            raw_text = str(display).replace(",", ".") if display is not None else ""

        c = _color(value)
        return f"""
        <div style="margin-bottom:8px">
            <div style="font-size:11px;color:#333;display:flex;justify-content:space-between">
                <span>{lbl}</span><span style="color:#666">{raw_text}</span>
            </div>
            <div style="background:#eee;height:6px;border-radius:3px;">
                <div style="width:{value:.1f}%;background:{c};height:6px;border-radius:3px;"></div>
            </div>
        </div>"""

    ov_color = _color(overall_score)
    header = f"""
    <div style="background:#f9f1f1;padding:12px 16px;border-radius:10px;margin-bottom:15px;
                display:flex;justify-content:space-between;align-items:center;">
        <div>
            <div style="font-size:26px;font-weight:800;">{player}</div>
            <div style="font-size:12px;color:#555;">
                {pos} | {team} | {age} yrs | {league} | {minutes} mins
            </div>
            <div style="font-size:11px;color:#888;margin-top:2px;">
                Template: {position_group} · {league_template}
            </div>
        </div>
        <div style="background:{ov_color};color:white;padding:10px 18px;
                    font-size:20px;font-weight:800;border-radius:8px;">
            {overall_score:.0f}
        </div>
    </div>"""

    categories_html = ""
    for category, group in report_template.items():
        stats = [s for s in group["stats"] if s in player_percentiles.index]
        weights = group.get("weights", {})
        score = calculate_weighted_score(stats, weights, player_percentiles)
        cat_color = _color(score)

        cat_header = f"""
        <div style="background:#f9f1f1;padding:8px 12px;margin:12px 0 8px;
                    display:flex;justify-content:space-between;align-items:center;">
            <b style="font-size:13px">{category}</b>
            <span style="background:{cat_color};color:white;padding:2px 8px;
                         border-radius:8px;font-size:12px;">{score:.0f}</span>
        </div>"""

        half = math.ceil(len(stats) / 2)
        left_bars = ""
        right_bars = ""
        for stat in stats[:half]:
            if stat in player_percentiles:
                left_bars += _bar(stat, player_percentiles[stat],
                                  player_data[stat] if stat in player_data else None)
        for stat in stats[half:]:
            if stat in player_percentiles:
                right_bars += _bar(stat, player_percentiles[stat],
                                   player_data[stat] if stat in player_data else None)

        categories_html += cat_header + f"""
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:0 20px;">
            <div>{left_bars}</div>
            <div>{right_bars}</div>
        </div>"""

    return f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
          background:#fff5f5; color:#222; padding:20px; max-width:900px; margin:0 auto; }}
</style></head>
<body>
{header}
{categories_html}
<div style="font-size:10px;color:#aaa;text-align:right;margin-top:12px;">JT Player Card</div>
</body></html>"""


# ══════════════════════════════════════════════════════════════════════════════
# 🔹 DISPLAY
# ══════════════════════════════════════════════════════════════════════════════

# Header
st.markdown(f"""
<div style="background:#f9f1f1;padding:12px 16px;border-radius:10px;margin-bottom:15px;
            display:flex;justify-content:space-between;align-items:center;">
    <div>
        <div style="font-size:30px;font-weight:800;">{player}</div>
        <div style="font-size:14px;color:#555;">
            {pos} | {team} | {age} yrs | {league} | {minutes} mins
        </div>
        <div style="font-size:12px;color:#888;margin-top:2px;">
            Template: {position_group} · {league_template} <br>
            Min: {min_score:.0f} | Avg: {avg_score:.0f} | Max: {max_score:.0f} | {score_mode.split()[0]} <br>
            Ranking: {player_rank} / {total_players}
        </div>
    </div>
    <div style="background:{color};color:white;padding:10px 18px;
                font-size:20px;font-weight:800;border-radius:8px;">
        {overall_score:.0f}
    </div>
</div>
""", unsafe_allow_html=True)

# Export button
card_html = build_card_html(
    player, pos, team, age, league, minutes, overall_score,
    category_scores, player_percentiles, player_data,
    report_template, position_group, league_template
)

st.download_button(
    label="⬇️ Download Player Card (HTML → open & screenshot)",
    data=card_html.encode("utf-8"),
    file_name=f"{player.replace(' ', '_')}_card.html",
    mime="text/html",
)

# ── Category sections ─────────────────────────────────────────────────────────
for category, group in report_template.items():
    stats   = [s for s in group["stats"] if s in player_percentiles.index]
    weights = group.get("weights", {})
    score   = calculate_weighted_score(stats, weights, player_percentiles)
    cat_color = get_color(score)

    st.markdown(f"""
        <div style="background:#f9f1f1;padding:12px 16px;margin-top:15px;margin-bottom:15px;
                    display:flex;justify-content:space-between;align-items:center;">
            <b>{category}</b>
            <span style="background:{cat_color};color:white;padding:2px 10px;border-radius:10px;">
                {score:.0f}
            </span>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    half = math.ceil(len(stats) / 2)

    with col1:
        for stat in stats[:half]:
            if stat in player_percentiles:
                stat_bar(stat, player_percentiles[stat],
                         player_data[stat] if stat in player_data else None)
    with col2:
        for stat in stats[half:]:
            if stat in player_percentiles:
                stat_bar(stat, player_percentiles[stat],
                         player_data[stat] if stat in player_data else None)
