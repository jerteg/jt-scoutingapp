import os
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

import streamlit as st
import pandas as pd

from shared.data_processing import preprocess_data
from ranking import (
    calculate_zscores,
    scale_zscores,
    apply_score_filters,
    calculate_rating,
    apply_league_adjustment,
)
from shared.templates import (
    template_config,
    role_config,
    position_groups,
    position_to_template,
    position_map,
    TOP5_LEAGUES,
    NEXT14_LEAGUES,
)

# ── Page config & custom CSS ──────────────────────────────────────────────────

st.set_page_config(layout="wide", page_title="JT Ranking Tool")

st.markdown("""
<style>
    /* Background */
    .stApp { background-color: #f5f0eb; }
    [data-testid="stSidebar"] { background-color: #ede8e1; }

    /* Sidebar headings */
    [data-testid="stSidebar"] h3 {
        color: #2d2d2d;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    /* Main title */
    h1 { color: #1a1a1a; font-weight: 800; }

    /* Dataframe */
    [data-testid="stDataFrame"] { border-radius: 8px; }

    /* Buttons */
    .stButton > button {
        background-color: #3d7a3d;
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
    }
    .stButton > button:hover { background-color: #2e5e2e; }

    /* Info / warning boxes */
    .stAlert { border-radius: 8px; }

    /* Role description badge */
    .role-desc {
        background: #e4ddd5;
        border-left: 4px solid #3d7a3d;
        padding: 8px 12px;
        border-radius: 4px;
        font-size: 0.85rem;
        color: #3a3a3a;
        margin-bottom: 12px;
    }

    /* Shortlist highlight */
    .shortlist-tag {
        background: #3d7a3d;
        color: white;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────

if "shortlist" not in st.session_state:
    st.session_state.shortlist = []

# ── Load data ─────────────────────────────────────────────────────────────────

data_path = os.path.join(BASE_DIR, "shared", "data.csv")
data = pd.read_csv(data_path)
data = preprocess_data(data)

data['Main Position'] = data['Position'].astype(str).str.split(',').str[0].str.strip()
data['Position Label'] = data['Main Position'].map(position_map).fillna(data['Main Position'])

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("JT Ranking Tool")
    st.markdown("---")

    # ── League template
    st.markdown("### 🏆 League Template")
    league_template = st.radio(
        "Competition scope",
        ["Top 5", "Next 14", "Both"],
        horizontal=True,
    )

    st.markdown("---")

    # ── Player filters
    st.markdown("### 🧍 Player")
    position_group = st.selectbox("Position", list(position_groups.keys()))

    # Role selection (based on position group)
    roles_for_position = role_config.get(position_group, {})
    role_options = ["— Custom (pick stats manually) —"] + list(roles_for_position.keys())
    selected_role = st.selectbox("Role", role_options)

    age_range    = st.slider("Age", 16, 40, (16, 40))
    value_range  = st.slider("Market Value", 0, 20_000_000, (0, 20_000_000), step=50_000)
    height_range = st.slider("Height", 150, 210, (150, 210))
    minutes_range = st.slider("Minutes played", 0, 10_000, (0, 10_000), step=100)
    foot = st.multiselect("Foot", ["left", "right", "both"])

    st.markdown("---")

    # ── Stats & weights
    st.markdown("### 📊 Performance")
    template_name  = position_to_template[position_group]
    template_stats = template_config[template_name]["stats"]

    use_role = selected_role != "— Custom (pick stats manually) —"

    if use_role:
        role_data   = roles_for_position[selected_role]
        stats       = list(role_data["stats"].keys())
        raw_weights = role_data["stats"]

        st.markdown(
            f'<div class="role-desc">📌 {role_data["description"]}</div>',
            unsafe_allow_html=True,
        )
        st.caption(f"Stats & weights pre-filled for **{selected_role}**")

        # Allow user to tweak weights
        st.markdown("#### ⚖️ Weights")
        weights = {}
        for stat in stats:
            weights[stat] = st.slider(
                stat, 0.0, 1.0, float(raw_weights[stat]), step=0.025
            )
    else:
        stats = st.multiselect("Select stats", template_stats, default=[])

        if not stats:
            st.info("Select stats to generate ranking")
            st.stop()

        st.markdown("#### 🎚️ Stat filters")
        score_filters_sidebar = {stat: st.slider(stat, 0, 100, (0, 100)) for stat in stats}

        st.markdown("#### ⚖️ Weights")
        default_w = 1 / len(stats)
        weights = {stat: st.slider(f"{stat} weight", 0.0, 1.0, default_w) for stat in stats}

    # Stat filters (for role mode, apply no percentile filter by default)
    if use_role:
        score_filters_sidebar = {stat: (0, 100) for stat in stats}

    total_w = sum(weights.values())
    if total_w == 0:
        st.warning("Total weight is 0 — adjust weights")
        st.stop()

    normalized_weights = {stat: w / total_w for stat, w in weights.items()}

# ── Filter & position data ────────────────────────────────────────────────────

positions     = position_groups[position_group]
position_data = data[data['Main Position'].isin(positions)].copy()

# League filter based on template
if league_template == "Top 5":
    position_data = position_data[position_data['League'].isin(TOP5_LEAGUES)]
elif league_template == "Next 14":
    position_data = position_data[position_data['League'].isin(NEXT14_LEAGUES)]
# "Both" → no filter

filtered_data = position_data[
    position_data['Age'].between(*age_range) &
    position_data['Market value'].between(*value_range) &
    position_data['Height'].between(*height_range) &
    position_data['Minutes played'].between(*minutes_range)
].copy()

if foot:
    filtered_data = filtered_data[filtered_data['Foot'].isin(foot)]

# ── Z-scores (on full position pool) ─────────────────────────────────────────

zscore_data  = calculate_zscores(position_data, stats)
scored_data  = scale_zscores(zscore_data, stats)
filtered_scores = apply_score_filters(scored_data, stats, score_filters_sidebar)

idx_key = ['Player', 'Team within selected timeframe']
final_df = filtered_scores[
    filtered_scores.set_index(idx_key).index.isin(
        filtered_data.set_index(idx_key).index
    )
]

# ── Ranking ───────────────────────────────────────────────────────────────────

ranking = calculate_rating(final_df, stats, normalized_weights)
ranking = apply_league_adjustment(ranking, league_template)

if ranking.empty:
    st.title(f"{position_group} Ranking")
    st.warning("⚠️ No players found with current filters")
    st.caption("Try adjusting filters (minutes, age, stats, etc.)")
    st.stop()

ranking = ranking.sort_values("Rating", ascending=False).reset_index(drop=True)
ranking["Rank"] = ranking.index + 1

# ── Main area ─────────────────────────────────────────────────────────────────

role_label = f" · {selected_role}" if use_role else ""
st.title(f"{position_group} Ranking{role_label}")

# ── Tabs: Ranking | Compare | Shortlist ──────────────────────────────────────

tab_ranking, tab_compare, tab_shortlist = st.tabs(["📊 Ranking", "⚖️ Compare", "⭐ Shortlist"])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 – RANKING
# ══════════════════════════════════════════════════════════════════════════════

with tab_ranking:
    col_search, col_export_xl, col_export_png = st.columns([4, 1, 1])

    with col_search:
        search = st.text_input("🔍 Search player", label_visibility="collapsed", placeholder="Search player…")

    display_ranking = ranking.copy()
    if search:
        display_ranking = display_ranking[
            display_ranking["Player"].str.contains(search, case=False, na=False)
        ]

    st.caption(f"{len(display_ranking)} players found  ·  League template: **{league_template}**  ·  Role: **{selected_role}**")

    display = (
        display_ranking[[
            'Rank', 'Player', 'Age', 'Position Label', 'Foot',
            'Team within selected timeframe', 'League', 'Rating'
        ]]
        .head(30)
        .rename(columns={
            "Team within selected timeframe": "Team",
            "Position Label": "Position",
        })
        .round(1)
    )

    display["Rank"]   = display["Rank"].astype(str)
    display["Rating"] = display["Rating"].map(lambda x: f"{x:.1f}")
    display["Age"]    = display["Age"].astype(str)

    st.dataframe(display, use_container_width=True, hide_index=True)

    # ── Add to shortlist ──────────────────────────────────────────────────────
    st.markdown("#### ⭐ Add to shortlist")
    player_options = display_ranking["Player"].head(30).tolist()
    to_add = st.selectbox("Select player to add", ["—"] + player_options, key="add_player")
    if st.button("Add to shortlist") and to_add != "—":
        if to_add not in st.session_state.shortlist:
            st.session_state.shortlist.append(to_add)
            st.success(f"{to_add} added to shortlist!")
        else:
            st.info(f"{to_add} is already in your shortlist.")

    # ── Export Excel ──────────────────────────────────────────────────────────
    with col_export_xl:
        excel_df = display.copy()
        from io import BytesIO
        buf = BytesIO()
        with pd.ExcelWriter(buf, engine="openpyxl") as writer:
            excel_df.to_excel(writer, index=False, sheet_name="Ranking")
        st.download_button(
            "📥 Excel",
            data=buf.getvalue(),
            file_name=f"{position_group}_ranking.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    # ── Export PNG via HTML table + instructions ──────────────────────────────
    with col_export_png:
        html_rows = "".join(
            f"<tr>{''.join(f'<td>{v}</td>' for v in row)}</tr>"
            for row in display.values.tolist()
        )
        header_cells = "".join(f"<th>{c}</th>" for c in display.columns)
        html_table = f"""
        <html><head><style>
            body {{ font-family: Arial, sans-serif; background: #f5f0eb; padding: 20px; }}
            h2 {{ color: #1a1a1a; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th {{ background: #3d7a3d; color: white; padding: 8px 12px; text-align: left; }}
            td {{ padding: 7px 12px; border-bottom: 1px solid #ddd; }}
            tr:nth-child(even) {{ background: #ede8e1; }}
        </style></head><body>
        <h2>{position_group} Ranking – {selected_role}</h2>
        <table><thead><tr>{header_cells}</tr></thead><tbody>{html_rows}</tbody></table>
        </body></html>
        """
        st.download_button(
            "🖼️ PNG*",
            data=html_table.encode(),
            file_name=f"{position_group}_ranking.html",
            mime="text/html",
            help="Download as HTML, then open in browser and use Ctrl+P → Save as PDF, or screenshot.",
        )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 – COMPARE
# ══════════════════════════════════════════════════════════════════════════════

with tab_compare:
    st.markdown("### ⚖️ Compare two players")
    all_players = ranking["Player"].tolist()

    col_a, col_b = st.columns(2)
    with col_a:
        player_a = st.selectbox("Player A", ["—"] + all_players, key="cmp_a")
    with col_b:
        player_b = st.selectbox("Player B", ["—"] + all_players, key="cmp_b")

    if player_a != "—" and player_b != "—" and player_a != player_b:
        row_a = ranking[ranking["Player"] == player_a].iloc[0]
        row_b = ranking[ranking["Player"] == player_b].iloc[0]

        compare_cols = ["Player", "Age", "Position Label", "Foot",
                        "Team within selected timeframe", "League", "Rating"]
        compare_cols += [f"{s}_score" for s in stats]

        def _fmt(row: pd.Series, key: str) -> str:
            val = row.get(key, "")
            if isinstance(val, float):
                return f"{val:.1f}"
            return str(val)

        rows = []
        for key in compare_cols:
            label = key.replace("_score", " (score)").replace("Team within selected timeframe", "Team")
            va, vb = _fmt(row_a, key), _fmt(row_b, key)
            rows.append({"Metric": label, player_a: va, player_b: vb})

        compare_df = pd.DataFrame(rows)
        st.dataframe(compare_df, use_container_width=True, hide_index=True)
    elif player_a == player_b and player_a != "—":
        st.info("Select two different players to compare.")
    else:
        st.info("Select two players above to compare them.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 – SHORTLIST
# ══════════════════════════════════════════════════════════════════════════════

with tab_shortlist:
    st.markdown("### ⭐ Shortlist")

    if not st.session_state.shortlist:
        st.info("Your shortlist is empty. Add players from the Ranking tab.")
    else:
        shortlist_df = ranking[ranking["Player"].isin(st.session_state.shortlist)][
            ['Rank', 'Player', 'Age', 'Position Label', 'Foot',
             'Team within selected timeframe', 'League', 'Rating']
        ].rename(columns={
            "Team within selected timeframe": "Team",
            "Position Label": "Position",
        }).round(1)

        shortlist_df["Rating"] = shortlist_df["Rating"].map(lambda x: f"{x:.1f}")
        st.dataframe(shortlist_df, use_container_width=True, hide_index=True)

        # Remove player
        to_remove = st.selectbox("Remove player", ["—"] + st.session_state.shortlist, key="rm_player")
        if st.button("Remove from shortlist") and to_remove != "—":
            st.session_state.shortlist.remove(to_remove)
            st.rerun()

        # Export shortlist to Excel
        buf2 = BytesIO()
        with pd.ExcelWriter(buf2, engine="openpyxl") as writer:
            shortlist_df.to_excel(writer, index=False, sheet_name="Shortlist")
        st.download_button(
            "📥 Export Shortlist (Excel)",
            data=buf2.getvalue(),
            file_name="shortlist.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
