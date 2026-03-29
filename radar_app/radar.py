import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from matplotlib.colors import LinearSegmentedColormap
from PIL import Image
from shared.templates import template_config


BASE_DIR = os.path.dirname(__file__)
logo_path = os.path.join(BASE_DIR, "target_scouting_black.png")

ts_logo = Image.open(logo_path)


def create_radar(data, player_name, player_team, template):

    # 🔹 config ophalen
    config = template_config[template]
    stats = config["stats"]
    positions = config["positions"]
    label = config["label"]

    data = data.copy()

    # 🔹 Main position bepalen
    data['Main Position'] = data['Position'].astype(str).str.split(',').str[0].str.strip()

    # 🔹 template dataset
    template_data = data[
        data['Main Position'].isin(positions)
    ]

    # 🔹 speler ophalen
    player_data = data[
        (data['Player'] == player_name) &
        (data['Team within selected timeframe'] == player_team)
    ]

    if player_data.empty:
        raise ValueError("Player not found")

    player_data = player_data.iloc[0]

    # 🔹 percentielen berekenen
    percentiles = template_data[stats].rank(pct=True) * 100
    negative_stats = config.get("negative_stats", [])

    for stat in negative_stats:
        if stat in percentiles.columns:
            percentiles[stat] = 100 - percentiles[stat]

    # 🔹 juiste speler selecteren (BELANGRIJK)
    player_mask = (
        (template_data['Player'] == player_name) &
        (template_data['Team within selected timeframe'] == player_team)
    )

    player_percentiles = percentiles[player_mask]

    if player_percentiles.empty:
        raise ValueError("Player percentiles not found")

    player_percentiles = player_percentiles.iloc[0]

    # 🔹 radar data
    angles = np.linspace(0, 2 * np.pi, len(stats), endpoint=False).tolist()
    values = player_percentiles.tolist()

    values += values[:1]
    angles += angles[:1]

    # 🔹 kleuren
    colors = ['red', 'orange', 'green']
    cmap = LinearSegmentedColormap.from_list("rg", colors, N=100)
    norm = plt.Normalize(0, 100)

    # 🔹 plot
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw={'projection': 'polar'})

    fig.patch.set_facecolor('#f9f1f1')
    ax.set_facecolor('#f9f1f1')

    # 🔹 achtergrond cirkel
    ax.fill(angles, [100] * len(angles), color='beige', alpha=0.2)

    # 🔹 bars
    ax.bar(
        angles,
        values,
        width=0.35,
        bottom=0,
        color=cmap(norm(values)),
        alpha=0.4,
        edgecolor='black'
    )

    # 🔹 waarden in chart
    for angle, value in zip(angles[:-1], values[:-1]):
        ax.text(
            angle,
            value / 1.1,
            f"{int(value)}",
            ha='center',
            va='center',
            fontsize=10,
            color='white',
            bbox=dict(facecolor='black', edgecolor='none', boxstyle='round,pad=0.3')
        )

    # 🔹 geen ticks
    ax.set_xticks([])
    ax.set_yticks([])

    # 🔹 labels splitsen
    def split_label(label, max_length=15):
        words = label.split()
        lines = []
        current = ""
        for word in words:
            if len(current) + len(word) > max_length:
                lines.append(current)
                current = ""
            current += word + " "
        lines.append(current)
        return "\n".join(lines)

    split_stats = [split_label(stat) for stat in stats]

    # 🔹 label rotatie (basis, werkt voor alle templates)
    rotate_stats = config.get("rotate_stats", [])

    for i, angle in enumerate(angles[:-1]):

        rotation = np.degrees(angle) + 90

        if stats[i] in rotate_stats:
            rotation += 180

        if rotation > 180:
            rotation -= 360

    # 🔹 alignment logic (zoals jij had)
        if stats[i] in rotate_stats:
            va = 'bottom'
        else:
            va = 'top'

        ax.text(
            angle,
            config.get("label_offset", 108),
            split_stats[i],
            ha='center',
            va=va,
            fontsize=9,
            color='#333333',
            rotation=rotation,
            rotation_mode='anchor'
        )

    # 🔹 logo
    ax_tslogo = fig.add_axes([0.84, 0.03, 0.1, 0.1])
    ax_tslogo.imshow(ts_logo)
    ax_tslogo.axis('off')

    # 🔹 titel info
    player_position = str(player_data['Position']).split(',')[0]
    player_age = player_data['Age']
    player_minutes = player_data['Minutes played']
    player_foot = player_data['Foot']

    ax.set_title(f"{player_name} ({player_age}) - {player_team}", size=22, pad=60)

    fig.text(
        0.5,
        0.94,
        f"{player_position} | {player_minutes} mins | {player_foot} | Next 14 Competitions | {label}".upper(),
        ha='center',
        fontsize=9.5,
        color='gray'
    )

    fig.text(0.05, 0.03, "Data: Wyscout (26/03/2026)", fontsize=9, color='gray')

    return fig