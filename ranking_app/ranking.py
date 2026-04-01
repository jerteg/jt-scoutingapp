import pandas as pd

from shared.templates import (
    LEAGUE_MULTIPLIERS_ALL,
    LEAGUE_MULTIPLIERS_NEXT14,
    TOP5_LEAGUES,
    NEXT14_LEAGUES,
)


def calculate_zscores(data: pd.DataFrame, stats: list[str]) -> pd.DataFrame:
    df = data.copy()
    for stat in stats:
        df[stat] = pd.to_numeric(df[stat], errors='coerce')
        mean, std = df[stat].mean(), df[stat].std()
        df[f"{stat}_z"] = 0 if std == 0 else (df[stat] - mean) / std
    return df


def scale_zscores(df: pd.DataFrame, stats: list[str]) -> pd.DataFrame:
    df = df.copy()
    for stat in stats:
        df[f"{stat}_score"] = df[f"{stat}_z"].rank(pct=True) * 100
        df[f"{stat}_score"] = df[f"{stat}_score"].fillna(50)
    return df


def apply_score_filters(
    df: pd.DataFrame,
    stats: list[str],
    score_filters: dict,
) -> pd.DataFrame:
    filtered = df.copy()
    for stat in stats:
        lo, hi = score_filters[stat]
        filtered = filtered[
            filtered[f"{stat}_score"].between(lo, hi)
        ]
    return filtered


def calculate_rating(
    df: pd.DataFrame,
    stats: list[str],
    weights: dict,
) -> pd.DataFrame:
    df = df.copy()
    total_weight = sum(weights.values())
    df["Rating"] = sum(df[f"{stat}_score"] * w for stat, w in weights.items()) / total_weight
    return df


def apply_league_adjustment(
    df: pd.DataFrame,
    league_template: str,   # "Top 5", "Next 14", or "Both"
) -> pd.DataFrame:
    """Multiply Rating by the league quality multiplier for eligible leagues."""
    df = df.copy()

    def _multiplier(league: str) -> float:
        if league_template == "Top 5":
            return LEAGUE_MULTIPLIERS_ALL.get(league, 1.0) if league in TOP5_LEAGUES else None
        if league_template == "Next 14":
            return LEAGUE_MULTIPLIERS_NEXT14.get(league, 1.0) if league in NEXT14_LEAGUES else None
        # "Both"
        return LEAGUE_MULTIPLIERS_ALL.get(league, 1.0)

    df["Rating"] = df.apply(
        lambda row: row["Rating"] * (_multiplier(row["League"]) or 1.0),
        axis=1,
    )
    return df
