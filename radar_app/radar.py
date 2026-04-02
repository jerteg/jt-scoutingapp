import importlib
import shared.templates

importlib.reload(shared.templates)

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from PIL import Image

import sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from shared.templates import template_config, TOP5_LEAGUES, NEXT14_LEAGUES, RADAR_CATEGORIES, ALL_RADAR_STATS, STAT_CATEGORY_COLORS, STAT_TO_CATEGORY, LEAGUE_DISPLAY_NAMES, FORCE_FLIP_STATS

# ── Logo ──────────────────────────────────────────────────────────────────────
_BASE = os.path.dirname(__file__)
_LOGO_PATH = os.path.join(_BASE, "target_scouting_black.png")
try:
    TS_LOGO = Image.open(_LOGO_PATH)
except FileNotFoundError:
    TS_LOGO = None

# ── Colors ────────────────────────────────────────────────────────────────────
BG_COLOR   = "#f5ede8"
CARD_COLOR = "#fdf6f2"
DARK_TEXT  = "#1a1a2e"
GRAY_TEXT  = "#6b6b7b"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _percentile_color(v):
    if v >= 90:   return "#0d9313"
    elif v >= 70: return "#3ebe43"
    elif v >= 50: return "#f39c12"
    elif v >= 25: return "#e67e22"
    else:         return "#e74c3c"


def _stat_short_label(stat: str) -> str:
    """Short display label for radar axis, with manual line breaks."""
    mapping = {
        "Passing accuracy (prog/1/3/forw)":        "Prog/F3/forw \n pass acc.",
        "PAdj Defensive duels won per 90":          "Def duels won\n/90",
        "PAdj Aerial duels won per 90":             "Aerial duels won\n/90",
        "PAdj Interceptions":                       "Interceptions",
        "Defensive duels won, %":                   "Def duels\nwon %",
        "Aerial duels won, %":                      "Aerial duels\nwon %",
        "Successful dribbles per received pass":    "Drib.\n/rec pass",
        "Successful dribbles, %":                   "Drib. %",
        "Progressive runs per received pass":       "Prog. runs\n/rec pass",
        "Completed progressive passes per 90":      "Prog. passes\n/90",
        "Completed passes to final third per 90":   "Passes F3\n/90",
        "Deep completions per 90":                  "Deep compl.\n/90",
        "Accurate crosses per received pass":       "Crosses\n/rec pass",
        "Shot assists per 90":                      "Shot ast.\n/90",
        "Key passes per pass":                      "Key passes\n/pass",
        "Touches in box per 90":                    "Box touches\n/90",
        "xG per shot":                              "xG/shot",
        "xG per 90":                                "xG/90",
        "xA per 90":                                "xA/90",
        "Finishing":                                "Finishing",
    }
    return mapping.get(stat, stat)


def _compute_percentiles(pool, player_name, player_team, stats):
    available = [s for s in stats if s in pool.columns]
    pct = pool[available].rank(pct=True) * 100

    for cat_data in RADAR_CATEGORIES.values():
        for s in cat_data.get("negative_stats", []):
            if s in pct.columns:
                pct[s] = 100 - pct[s]

    mask = (
        (pool["Player"] == player_name) &
        (pool["Team within selected timeframe"] == player_team)
    )
    if not mask.any():
        raise ValueError(f"Player '{player_name}' not found in pool.")
    return pct[mask].iloc[0]


def _build_pool(data, template_key, percentile_basis, player_league=None):
    pool = data.copy()
    pool["Main Position"] = pool["Position"].astype(str).str.split(",").str[0].str.strip()
    positions = template_config[template_key]["positions"]
    pool = pool[pool["Main Position"].isin(positions)]

    if percentile_basis == "T5 only":
        pool = pool[pool["League"].isin(TOP5_LEAGUES)]
    elif percentile_basis == "Next 14 only":
        pool = pool[pool["League"].isin(NEXT14_LEAGUES)]
    elif percentile_basis == "Own league" and player_league:
        pool = pool[pool["League"] == player_league]
    # "T5 + Next 14" → no extra filter
    return pool


# ── Legend ────────────────────────────────────────────────────────────────────

def _add_legend(fig, rect=(0.00, 0.022, 0.85, 0.07)):
    """
    Horizontal percentile legend.
    rect is narrow on purpose — logo sits to the right of it.
    """
    legend_items = [
        (">= 90 \n (Top 10%)",                   "#0d9313"),
        ("70 - 89 (Way \nabove average)",        "#3ebe43"),
        ("50 – 69  (Slightly \nabove average)",  "#f39c12"),
        ("25 – 49  \n(Below average)",           "#e67e22"),
        ("< 25  \n(Bottom 25%)",                 "#e74c3c"),
    ]
        
    ax_leg = fig.add_axes(rect)
    ax_leg.set_axis_off()
    ax_leg.set_xlim(0, 1)
    ax_leg.set_ylim(0, 1)

    n   = len(legend_items)
    w = 0.1
    gap = 0.07

    start_x = 0.02
    
    for i, (label, color) in enumerate(legend_items):
        x = start_x + i * (w + gap)
        ax_leg.add_patch(
            mpatches.FancyBboxPatch(
                (x, 0.05), w, 0.85,
                boxstyle="round,pad=0.02",
                facecolor=color, alpha=0.35,
                edgecolor=color, linewidth=1.2,
            )
        )
        ax_leg.text(
            x + w / 2, 0.52, label,
            ha="center", va="center",
            fontsize=7.5, color=DARK_TEXT, fontweight="bold",
        )


# ── Core draw routine ─────────────────────────────────────────────────────────

def _draw_radar(ax, stats, angles, values, bar_width_ratio=0.75):
    """
    Draw bars, category arcs, category labels, and stat labels on a polar ax.
    No background rings, no spokes, no fill.
    """
    n         = len(stats)
    bar_width = (2 * np.pi / n) * bar_width_ratio
    half_w    = bar_width / 2

    # ── Bars ──────────────────────────────────────────────────────────────────
    for angle, value, stat in zip(angles, values, stats):
        ax.bar(
            angle, value,
            width=bar_width,
            bottom=0,
            color=_percentile_color(value),
            alpha=0.55,
            edgecolor="black",
            linewidth=0.6,
            zorder=2,
        )
        if value > 6:
            ax.text(
                angle, value / 1.15,
                str(int(round(value))),
                ha="center", va="center",
                fontsize=8, color="white", fontweight="bold",
                bbox=dict(facecolor="black", edgecolor="none",
                          boxstyle="round,pad=0.25"),
                zorder=3,
            )

    # ── Category arcs + labels ────────────────────────────────────────────────
    ARC_R  = 108   # coloured arc radius
    CAT_R  = 119   # category name radius
    STAT_R = 133   # stat label radius

    cat_angle_map = {}
    for i, stat in enumerate(stats):
        cat = STAT_TO_CATEGORY.get(stat, "")
        cat_angle_map.setdefault(cat, []).append(angles[i])

    for cat, cat_angles in cat_angle_map.items():
        cat_color = RADAR_CATEGORIES[cat]["color"]
        a_start   = min(cat_angles) - half_w * 0.9
        a_end     = max(cat_angles) + half_w * 0.9
        arc       = np.linspace(a_start, a_end, 80)

        ax.plot(arc, [ARC_R] * 80,
                color=cat_color, linewidth=5,
                solid_capstyle="round", zorder=4)

        # Category label — tangential, always readable
        mid_rad = (a_start + a_end) / 2
        mid_deg = np.degrees(mid_rad) % 360

        rot = mid_deg - 90
        if 90 < mid_deg <= 270:
            rot += 180

        ax.text(
            mid_rad, CAT_R,
            cat.upper(),
            ha="center", va="center",
            fontsize=7, fontweight="bold", color=cat_color,
            rotation=rot, rotation_mode="anchor",
            zorder=5,
        )

    # ── Stat labels ───────────────────────────────────────────────────────────

 

    for angle, stat in zip(angles, stats):
        label = _stat_short_label(stat)
        deg   = np.degrees(angle) % 360

        rot = deg - 90

        if stat in FORCE_FLIP_STATS:
            rot += 180
        else:
            if deg > 180:
                rot += 180

        ax.text(
            angle, STAT_R,
            label,
            ha="center", va="center",
            fontsize=7, color=DARK_TEXT,
            rotation=rot, rotation_mode="anchor",
            linespacing=1.4, zorder=5,
        )

    # ── Axes cleanup ──────────────────────────────────────────────────────────
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_ylim(0, 152)
    ax.spines["polar"].set_visible(False)
    ax.set_facecolor(CARD_COLOR)


# ── Public API ────────────────────────────────────────────────────────────────

def create_radar(
    data,
    player_name,
    player_team,
    template_key,
    percentile_basis="T5 + Next 14",
):
    stats  = ALL_RADAR_STATS
    angles = np.linspace(0, 2 * np.pi, len(stats), endpoint=False).tolist()

    player_row = data[
        (data["Player"] == player_name) &
        (data["Team within selected timeframe"] == player_team)
    ]
    if player_row.empty:
        raise ValueError(f"Player '{player_name}' not found.")
    player_row    = player_row.iloc[0]
    player_league = player_row.get("League", None)

    pool   = _build_pool(data, template_key, percentile_basis, player_league)
    pct    = _compute_percentiles(pool, player_name, player_team, stats)
    values = [float(pct.get(s, 0)) for s in stats]

    # ── Figure ────────────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(11, 12.5))
    fig.patch.set_facecolor(BG_COLOR)

    ax = fig.add_axes([0.01, 0.12, 0.92, 0.78], projection="polar")
    _draw_radar(ax, stats, angles, values)

    # ── Header ────────────────────────────────────────────────────────────────
    pos    = str(player_row.get("Position", "")).split(",")[0].strip()
    age    = player_row.get("Age", "")
    mins   = player_row.get("Minutes played", "")
    foot   = player_row.get("Foot", "")
    league = LEAGUE_DISPLAY_NAMES.get(player_league, player_league or "")

    fig.text(
        0.5, 0.965,
        f"{player_name}  ({age})  —  {player_team}",
        ha="center", fontsize=18, fontweight="bold", color=DARK_TEXT,
    )
    fig.text(
        0.5, 0.946,
        f"{pos}  |  {mins} mins  |  {foot}  |  {league}  |  Percentile basis: {percentile_basis}",
        ha="center", fontsize=8.5, color=GRAY_TEXT,
    )

    # ── Legend + logo ─────────────────────────────────────────────────────────
    # Legend pills: x=0.05 → 0.77, logo: x=0.865 → 0.955
    _add_legend(fig, rect=(0.00, 0.022, 0.85, 0.07))
    fig.text(0.00, 0.007, "Data: Wyscout (26/03/2026)", fontsize=7.5, color=GRAY_TEXT)

    if TS_LOGO:
        ax_logo = fig.add_axes([0.865, 0.012, 0.09, 0.065])
        ax_logo.imshow(TS_LOGO)
        ax_logo.axis("off")

    return fig


def create_comparison_radar(
    data,
    player1_name, player1_team,
    player2_name, player2_team,
    template_key,
    percentile_basis="T5 + Next 14",
    mode="side_by_side",
):
    """
    mode: "side_by_side"  → two radars side by side
          "overlay"       → both players in one radar
    """
    stats  = ALL_RADAR_STATS
    angles = np.linspace(0, 2 * np.pi, len(stats), endpoint=False).tolist()

    COLOR1, COLOR2 = "#2980b9", "#c0392b"

    def _get_row(name, team):
        row = data[(data["Player"] == name) &
                   (data["Team within selected timeframe"] == team)]
        if row.empty:
            raise ValueError(f"Player '{name}' not found.")
        return row.iloc[0]

    p1 = _get_row(player1_name, player1_team)
    p2 = _get_row(player2_name, player2_team)

    pool1 = _build_pool(data, template_key, percentile_basis, p1.get("League"))
    pool2 = _build_pool(data, template_key, percentile_basis, p2.get("League"))
    vals1 = [float(_compute_percentiles(pool1, player1_name, player1_team, stats).get(s, 0)) for s in stats]
    vals2 = [float(_compute_percentiles(pool2, player2_name, player2_team, stats).get(s, 0)) for s in stats]

    # ── Side by side ──────────────────────────────────────────────────────────
    if mode == "side_by_side":
        fig, axes = plt.subplots(1, 2, figsize=(22, 12.5),
                                 subplot_kw={"projection": "polar"})
        fig.patch.set_facecolor(BG_COLOR)

        for ax, vals, name, team, row in [
            (axes[0], vals1, player1_name, player1_team, p1),
            (axes[1], vals2, player2_name, player2_team, p2),
        ]:
            _draw_radar(ax, stats, angles, vals)
            pos   = str(row.get("Position", "")).split(",")[0].strip()
            age   = row.get("Age", "")
            mins  = row.get("Minutes played", "")
            ldisp = LEAGUE_DISPLAY_NAMES.get(row.get("League"), row.get("League", ""))
            ax.set_title(
                f"{name}  ({age})  —  {team}\n{pos}  |  {mins} mins  |  {ldisp}",
                fontsize=12, fontweight="bold", color=DARK_TEXT, pad=70,
            )

        fig.suptitle("Player Comparison", fontsize=20,
                     fontweight="bold", color=DARK_TEXT, y=0.98)
        _add_legend(fig, rect=(0.20, 0.022, 0.55, 0.055))
        fig.text(0.02, 0.007, "Data: Wyscout (26/03/2026)", fontsize=7.5, color=GRAY_TEXT)
        if TS_LOGO:
            ax_logo = fig.add_axes([0.91, 0.010, 0.06, 0.050])
            ax_logo.imshow(TS_LOGO)
            ax_logo.axis("off")

    # ── Overlay ───────────────────────────────────────────────────────────────
    else:
        fig = plt.figure(figsize=(12, 13))
        fig.patch.set_facecolor(BG_COLOR)
        ax = fig.add_axes([0.05, 0.12, 0.90, 0.78], projection="polar")
        ax.set_facecolor(CARD_COLOR)

        n         = len(stats)
        bar_width = (2 * np.pi / n) * 0.35
        half_w    = bar_width / 2

        for angle, v1, v2, stat in zip(angles, vals1, vals2, stats):
            ax.bar(angle - half_w * 0.27, v1, width=bar_width * 0.46,
                   bottom=0, color=COLOR1, alpha=0.55,
                   edgecolor="black", linewidth=0.5, zorder=2)
            ax.bar(angle + half_w * 0.27, v2, width=bar_width * 0.46,
                   bottom=0, color=COLOR2, alpha=0.55,
                   edgecolor="black", linewidth=0.5, zorder=2)
            if v1 > 6:
                ax.text(angle - half_w * 0.27, v1 / 1.15,
                        str(int(round(v1))), ha="center", va="center",
                        fontsize=7, color="white", fontweight="bold",
                        bbox=dict(facecolor="black", edgecolor="none",
                                  boxstyle="round,pad=0.2"), zorder=3)
            if v2 > 6:
                ax.text(angle + half_w * 0.27, v2 / 1.15,
                        str(int(round(v2))), ha="center", va="center",
                        fontsize=7, color="white", fontweight="bold",
                        bbox=dict(facecolor="black", edgecolor="none",
                                  boxstyle="round,pad=0.2"), zorder=3)

        # Category arcs + labels + stat labels (same logic as _draw_radar)
        ARC_R, CAT_R, STAT_R = 108, 119, 133
        cat_angle_map = {}
        for i, stat in enumerate(stats):
            cat = STAT_TO_CATEGORY.get(stat, "")
            cat_angle_map.setdefault(cat, []).append(angles[i])

        for cat, cat_angles in cat_angle_map.items():
            cat_color = RADAR_CATEGORIES[cat]["color"]
            a_start   = min(cat_angles) - half_w * 0.9
            a_end     = max(cat_angles) + half_w * 0.9
            arc       = np.linspace(a_start, a_end, 80)
            ax.plot(arc, [ARC_R] * 80, color=cat_color, linewidth=5,
                    solid_capstyle="round", zorder=4)
            mid_rad = (a_start + a_end) / 2
            mid_deg = np.degrees(mid_rad) % 360
            rot = mid_deg - 90
            if 90 < mid_deg <= 270:
                rot += 180
            ax.text(mid_rad, CAT_R, cat.upper(),
                    ha="center", va="center",
                    fontsize=7, fontweight="bold", color=cat_color,
                    rotation=rot, rotation_mode="anchor", zorder=5)

        for angle, stat in zip(angles, stats):
            label = _stat_short_label(stat)
            deg   = np.degrees(angle) % 360
            rot   = deg - 90
            if 90 < deg <= 270:
                rot += 180
            ax.text(angle, STAT_R, label,
                    ha="center", va="center",
                    fontsize=7, color=DARK_TEXT,
                    rotation=rot, rotation_mode="anchor",
                    linespacing=1.4, zorder=5)

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_ylim(0, 152)
        ax.spines["polar"].set_visible(False)

        # Player colour legend
        p1_disp = LEAGUE_DISPLAY_NAMES.get(p1.get("League"), p1.get("League", ""))
        p2_disp = LEAGUE_DISPLAY_NAMES.get(p2.get("League"), p2.get("League", ""))
        patch1 = mpatches.Patch(color=COLOR1, alpha=0.7,
            label=f"{player1_name} ({p1.get('Age')}) — {player1_team} | {p1_disp}")
        patch2 = mpatches.Patch(color=COLOR2, alpha=0.7,
            label=f"{player2_name} ({p2.get('Age')}) — {player2_team} | {p2_disp}")
        ax.legend(handles=[patch1, patch2], loc="upper right",
                  bbox_to_anchor=(1.18, 1.14), fontsize=9,
                  frameon=True, facecolor=CARD_COLOR, edgecolor="#e0c8be")

        fig.suptitle("Player Comparison — Overlay", fontsize=18,
                     fontweight="bold", color=DARK_TEXT, y=0.975)

        _add_legend(fig, rect=(0.20, 0.022, 0.55, 0.055))
        fig.text(0.05, 0.007, "Data: Wyscout (26/03/2026)", fontsize=7.5, color=GRAY_TEXT)
        if TS_LOGO:
            ax_logo = fig.add_axes([0.865, 0.012, 0.09, 0.065])
            ax_logo.imshow(TS_LOGO)
            ax_logo.axis("off")

    return fig
