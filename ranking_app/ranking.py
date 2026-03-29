import pandas as pd
import streamlit as st


def calculate_zscores(data, stats):

    df = data.copy()

    for stat in stats:
        df[stat] = pd.to_numeric(df[stat], errors='coerce')

        mean = df[stat].mean()
        std = df[stat].std()

        if std == 0:
            df[f"{stat}_z"] = 0
        else:
            df[f"{stat}_z"] = (df[stat] - mean) / std

    return df


def scale_zscores(df, stats):
    df = df.copy()

    for stat in stats:
        df[f"{stat}_score"] = df[f"{stat}_z"].rank(pct=True) * 100

        # 🔥 CRUCIAAL
        df[f"{stat}_score"] = df[f"{stat}_score"].fillna(50)

    return df


def apply_score_filters(df, stats, score_filters):

    filtered = df.copy()

    for stat in stats:
        min_s, max_s = score_filters[stat]

        before = len(filtered)

        filtered = filtered[
            (filtered[f"{stat}_score"] >= min_s) &
            (filtered[f"{stat}_score"] <= max_s)
        ]

        after = len(filtered)

    return filtered

def calculate_rating(df, stats, weights):
    df = df.copy()

    total_weight = sum(weights.values())

    df["Rating"] = 0

    for stat in stats:
        df["Rating"] += df[f"{stat}_score"] * weights[stat]

    df["Rating"] = df["Rating"] / total_weight

    return df
