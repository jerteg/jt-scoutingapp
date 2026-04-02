import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from scipy.stats import percentileofscore

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'shared'))

from data_processing import preprocess_data
from templates import position_groups, template_config

# ── constants ──────────────────────────────────────────────────────────────────

BG_COLOR = "#eee8df"  # warm beige matching the ranking tool

REPORT_STATS = {
    "Goalscoring": [
        "Non-penalty goals per 90",
        "xG per 90",
        "xG per shot",
        "Finishing",
        "Shots per 90",
        "Shots on target, %",
        "Touches in box per 90",
    ],
    "Chance creation": [
        "Assists per 90",
        "xA per 90",
        "Shot assists per 90",
        "Key passes per pass",
        "Through passes per pass",
        "Accurate crosses per received pass",
        "Accurate crosses, %",
    ],
    "Dribbling": [
        "Successful dribbles per received pass",
        "Successful dribbles, %",
        "Progressive runs per received pass",
    ],
    "Passing": [
        "Completed progressive passes per 90",
        "Accurate progressive passes, %",
        "Completed passes to final third per 90",
        "Accurate passes to final third, %",
        "Completed passes to penalty area per 90",
        "Accurate passes to penalty area, %",
        "Deep completions per 90",
    ],
    "Defending": [
        "PAdj Defensive duels won per 90",
        "Defensive duels won, %",
        "PAdj Aerial duels won per 90",
        "Aerial duels won, %",
        "PAdj Interceptions",
        "PAdj Successful defensive actions per 90",
        "Fouls per 90",
    ],
}

EXPORT_PRESETS = {
    "Default (16:9)": (1200, 675),
    "Square (1:1)":   (800,  800),
    "Portrait (3:4)": (675,  900),
    "Wide (2:1)":     (1200, 600),
}

# ── helpers ────────────────────────────────────────────────────────────────────

@st.cache_data
def load_data():
    base = os.path.join(os.path.dirname(__file__), '..', 'shared', 'data.csv')
    df = pd.read_csv(base)
    df = preprocess_data(df)
    if "Position" in df.columns:
        df["Main Position"] = (
            df["Position"].astype(str).str.split(",").str[0].str.strip()
        )
    return df


def build_stat_options(available_cols: set) -> list:
    """Return list of (display_label, stat_key | None) tuples.
    None = category separator (not selectable)."""
    options = []
    for category, stats in REPORT_STATS.items():
        options.append((f"── {category} ──", None))
        for stat in stats:
            if stat in available_cols:
                options.append((stat, stat))
    return options


def compute_percentile_score(df_ref: pd.DataFrame, player_row: pd.Series,
                              x_stat: str, y_stat: str) -> float:
    scores = []
    for stat in [x_stat, y_stat]:
        col = df_ref[stat].dropna()
        scores.append(
            percentileofscore(col, player_row[stat], kind="rank") if not col.empty else 50.0
        )
    return float(np.mean(scores))


def percentile_color(score: float) -> str:
    """Gradient red (0) → orange (50) → green (100)."""
    if score <= 50:
        t = score / 50.0
        r = int(220 + t * 35)
        g = int(50  + t * 115)
        b = int(50  - t * 50)
    else:
        t = (score - 50) / 50.0
        r = int(255 - t * 205)
        g = int(165 + t * 35)
        b = int(0   + t * 50)
    return f"rgb({r},{g},{b})"


# ── page ───────────────────────────────────────────────────────────────────────

def main():
    st.set_page_config(page_title="Scatter Plot", layout="wide")

    st.markdown(
        f"""
        <style>
        [data-testid="stAppViewContainer"],
        [data-testid="stHeader"] {{
            background-color: {BG_COLOR};
        }}
        section[data-testid="stSidebar"] {{
            background-color: {BG_COLOR};
        }}
        section[data-testid="stSidebar"] * {{
            color: #1a1a1a !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    df = load_data()

    # ── column detection ───────────────────────────────────────────────────────
    name_col = "Player"
    comp_col = next((c for c in df.columns if "league" in c.lower()
                     or "competition" in c.lower()), None)
    team_col = next((c for c in df.columns if c.lower() in ("team", "club")), None)
    age_col  = next((c for c in df.columns if c.lower() == "age"), None)
    min_col  = next((c for c in df.columns if "minute" in c.lower()), None)

    # ── sidebar ────────────────────────────────────────────────────────────────
    st.sidebar.title("JT Scatter Plot Tool")
    st.sidebar.markdown("---")
    st.sidebar.header("Filters")

    # 1. Position
    selected_position = st.sidebar.selectbox("Position", list(position_groups.keys()))
    pos_codes = position_groups[selected_position]
    df_pos = df[df["Main Position"].isin(pos_codes)].copy()

    # 2. Competition
    if comp_col:
        all_comps = sorted(df_pos[comp_col].dropna().unique())
        selected_comps = st.sidebar.multiselect("Competition", all_comps, default=all_comps)
        df_pos = df_pos[df_pos[comp_col].isin(selected_comps)]

    # 3. Club search
    if team_col:
        club_options = ["All clubs"] + sorted(df_pos[team_col].dropna().unique())
        selected_club = st.sidebar.selectbox("Filter by club (optional)", club_options)
        if selected_club != "All clubs":
            df_pos = df_pos[df_pos[team_col] == selected_club]

    # 4. Player highlight
    player_options = ["None"] + sorted(df_pos[name_col].dropna().unique())
    highlighted_player = st.sidebar.selectbox("Highlight player (optional)", player_options)

    # 5. Age
    if age_col and not df_pos.empty:
        lo, hi = int(df_pos[age_col].min()), int(df_pos[age_col].max())
        age_range = st.sidebar.slider("Age", lo, hi, (lo, hi))
        df_pos = df_pos[df_pos[age_col].between(*age_range)]

    # 6. Minutes
    if min_col and not df_pos.empty:
        max_min = int(df_pos[min_col].max())
        min_minutes = st.sidebar.slider(
            "Minimum minutes played", 0, max_min, min(500, max_min), step=50
        )
        df_pos = df_pos[df_pos[min_col] >= min_minutes]

    st.sidebar.markdown(f"**{len(df_pos)} players** after filtering")
    st.sidebar.markdown("---")

    # ── axes ───────────────────────────────────────────────────────────────────
    st.sidebar.header("Axes")

    available_cols = set(df_pos.columns)
    stat_options   = build_stat_options(available_cols)
    labels         = [lbl for lbl, _ in stat_options]
    keys           = [key for _, key in stat_options]
    real_idx       = [i for i, k in enumerate(keys) if k is not None]

    def stat_selectbox(label, default_pos):
        idx = st.sidebar.selectbox(
            label,
            options=real_idx,
            index=default_pos,
            format_func=lambda i: labels[i],
        )
        return keys[idx]

    x_stat = stat_selectbox("X-axis", 0)
    y_stat = stat_selectbox("Y-axis", min(1, len(real_idx) - 1))

    # Bubble size
    size_candidates = [min_col, "Shots per 90", "Passes per 90",
                       "Dribbles per 90", "Aerial duels per 90"]
    size_options = [None] + [c for c in size_candidates if c and c in available_cols]
    size_stat = st.sidebar.selectbox(
        "Bubble size (optional)", size_options, format_func=lambda x: x or "Equal"
    )

    st.sidebar.markdown("---")
    st.sidebar.header("Labels & colours")

    show_percentile  = st.sidebar.checkbox("Colour by percentile (X + Y)", value=False)
    show_top_labels  = st.sidebar.checkbox("Show names: top N players", value=False)
    top_n = st.sidebar.slider("Top N to label", 3, 30, 10) if show_top_labels else 0
    show_all_labels  = st.sidebar.checkbox("Show all player names", value=False)

    st.sidebar.markdown("---")
    st.sidebar.header("Export")

    preset_name = st.sidebar.selectbox("Plot dimensions", list(EXPORT_PRESETS.keys()))
    plot_w, plot_h = EXPORT_PRESETS[preset_name]

    # ── build data ─────────────────────────────────────────────────────────────
    plot_df = df_pos.dropna(subset=[x_stat, y_stat]).copy()

    if plot_df.empty:
        st.warning("No players found with the current filters.")
        return

    # Compute percentile scores for everyone (needed for top-N labels too)
    plot_df["_pct"] = plot_df.apply(
        lambda row: compute_percentile_score(plot_df, row, x_stat, y_stat), axis=1
    )

    top_n_names: set = set(
        plot_df.nlargest(top_n, "_pct")[name_col].tolist()
    ) if show_top_labels else set()

    # Bubble sizes
    if size_stat and size_stat in plot_df.columns:
        raw = plot_df[size_stat].fillna(0)
        sizes = ((raw - raw.min()) / (raw.max() - raw.min() + 1e-9)) * 28 + 7
    else:
        sizes = pd.Series([10.0] * len(plot_df), index=plot_df.index)

    is_highlighted = highlighted_player != "None"

    # ── build figure ───────────────────────────────────────────────────────────
    fig = go.Figure()

    for i, (idx, row) in enumerate(plot_df.iterrows()):
        pname        = row[name_col]
        is_this      = pname == highlighted_player
        pct          = row["_pct"]
        base_size    = float(sizes.loc[idx])

        if is_highlighted:
            if is_this:
                color    = "#FFD700"
                opacity  = 1.0
                msize    = base_size * 1.9
                lw, lc   = 2.5, "#333"
                symbol   = "star"
            else:
                color    = "#999999"
                opacity  = 0.28
                msize    = base_size
                lw, lc   = 0, "rgba(0,0,0,0)"
                symbol   = "circle"
        else:
            color    = percentile_color(pct) if show_percentile else "#4C9BE8"
            opacity  = 0.85
            msize    = base_size
            lw, lc   = 0.5, "rgba(255,255,255,0.4)"
            symbol   = "circle"

        hover_lines = [f"<b>{pname}</b>"]
        if team_col and comp_col:
            hover_lines.append(f"{row.get(team_col,'')} · {row.get(comp_col,'')}")
        elif team_col:
            hover_lines.append(str(row.get(team_col, "")))

        show_label = show_all_labels or (show_top_labels and pname in top_n_names) or is_this

        fig.add_trace(go.Scatter(
            x=[row[x_stat]],
            y=[row[y_stat]],
            mode="markers",
            marker=dict(size=msize, color=color, opacity=opacity,
                        line=dict(width=lw, color=lc), symbol=symbol),
            hovertemplate="<br>".join(hover_lines) + "<extra></extra>",
            showlegend=False,
        ))

        # Inline text label (show_all_labels case handled via annotations below)
        if show_label and not show_top_labels:
            fig.add_annotation(
                x=row[x_stat], y=row[y_stat],
                text=pname,
                showarrow=False,
                yshift=13,
                font=dict(size=9, color="white"),
                bgcolor="rgba(0,0,0,0.72)",
                borderpad=2,
            )

    # Top-N annotations (black pill labels)
    if show_top_labels:
        for _, row in plot_df.nlargest(top_n, "_pct").iterrows():
            pname = row[name_col]
            if is_highlighted and pname == highlighted_player:
                continue
            fig.add_annotation(
                x=row[x_stat], y=row[y_stat],
                text=pname,
                showarrow=False,
                yshift=13,
                font=dict(size=9, color="white"),
                bgcolor="rgba(0,0,0,0.75)",
                borderpad=3,
            )

    # All-player name annotations
    if show_all_labels and not show_top_labels:
        for _, row in plot_df.iterrows():
            pname = row[name_col]
            if is_highlighted and pname == highlighted_player:
                continue
            fig.add_annotation(
                x=row[x_stat], y=row[y_stat],
                text=pname,
                showarrow=False,
                yshift=13,
                font=dict(size=8, color="white"),
                bgcolor="rgba(0,0,0,0.65)",
                borderpad=2,
            )

    # Highlighted player annotation (always on top)
    if is_highlighted:
        hp_rows = plot_df[plot_df[name_col] == highlighted_player]
        if not hp_rows.empty:
            hp = hp_rows.iloc[0]


    # Mean lines
    fig.add_vline(x=plot_df[x_stat].mean(),
                  line=dict(color="rgba(60,60,60,0.3)", dash="dot", width=1))
    fig.add_hline(y=plot_df[y_stat].mean(),
                  line=dict(color="rgba(60,60,60,0.3)", dash="dot", width=1))

    fig.update_layout(
        paper_bgcolor=BG_COLOR,
        plot_bgcolor=BG_COLOR,
        width=plot_w,
        height=plot_h,
        margin=dict(l=70, r=40, t=85, b=70),
        title=dict(
            text=(
                f"<b>{x_stat}</b>  vs  <b>{y_stat}</b>"
                f"<br><sup>{selected_position} · {len(plot_df)} players</sup>"
            ),
            font=dict(size=20, color="#1a1a1a"),
            x=0.02,
        ),
        xaxis=dict(
            title=dict(text=x_stat, font=dict(color="#1a1a1a", size=20)),
            tickfont=dict(color="#333"),
            gridcolor="rgba(0,0,0,0.07)",
            linecolor="rgba(0,0,0,0.15)",
            zeroline=False,
        ),
        yaxis=dict(
            title=dict(text=y_stat, font=dict(color="#1a1a1a", size=20)),
            tickfont=dict(color="#333"),
            gridcolor="rgba(0,0,0,0.07)",
            linecolor="rgba(0,0,0,0.15)",
            zeroline=False,
        ),
        hoverlabel=dict(
            bgcolor="#1a1a1a",
            bordercolor="rgba(255,255,255,0.15)",
            font=dict(size=12, color="white"),
        ),
    )

    st.plotly_chart(fig, use_container_width=False)

    # Percentile legend
    if show_percentile:
        st.markdown(
            """
            <div style="display:flex;gap:8px;align-items:center;
                        margin-top:4px;margin-bottom:12px;">
              <span style="background:rgb(220,50,50);padding:2px 10px;
                border-radius:4px;font-size:12px;color:white;">low</span>
              <span style="background:rgb(255,165,0);padding:2px 10px;
                border-radius:4px;font-size:12px;color:white;">average</span>
              <span style="background:rgb(50,200,50);padding:2px 10px;
                border-radius:4px;font-size:12px;color:white;">high</span>
              <span style="font-size:11px;color:#555;">
                Combined percentile of X &amp; Y stat within position group
              </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Raw data table
    with st.expander("📋 View raw data"):
        show_cols = (
            [name_col]
            + ([team_col] if team_col else [])
            + ([comp_col] if comp_col else [])
            + ([age_col]  if age_col  else [])
            + [x_stat, y_stat]
            + ([size_stat] if size_stat else [])
            + ["_pct"]
        )
        show_cols = [c for c in show_cols if c in plot_df.columns]
        st.dataframe(
            plot_df[show_cols]
            .rename(columns={"_pct": "Percentile score (X+Y)"})
            .sort_values("Percentile score (X+Y)", ascending=False)
            .reset_index(drop=True),
            use_container_width=True,
        )


if __name__ == "__main__":
    main()