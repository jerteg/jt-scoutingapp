import pandas as pd


def _to_float(series: pd.Series) -> pd.Series:
    """Normalize comma-decimal strings and coerce to float."""
    return pd.to_numeric(series.astype(str).str.replace(',', '.', regex=False), errors='coerce')


def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:
    data = data.copy()

    # ── helpers ──────────────────────────────────────────────────────────────
    cols = [
        'xG', 'Shots', 'Goals per 90', 'xG per 90',
        'Passes per 90', 'Key passes per 90', 'Through passes per 90',
        'Dribbles per 90', 'Successful dribbles, %',
        'Successful dribbles per 90', 'Received passes per 90',
        'Crosses per 90', 'Accurate crosses, %',
        'Defensive duels per 90', 'Defensive duels won, %',
        'Aerial duels per 90', 'Aerial duels won, %',
        'Progressive passes per 90', 'Forward passes per 90',
        'Accurate progressive passes, %',
        'Passes to final third per 90', 'Accurate passes to final third, %',
        'Passes to penalty area per 90', 'Accurate passes to penalty area, %',
        'Deep completions per 90',
        'Accurate forward passes, %',
        'Progressive runs per 90',
        'Successful defensive actions per 90',
        'PAdj Interceptions',
        'Touches in box per 90', 'Fouls suffered per 90',
        'Non-penalty goals per 90', 'Shots per 90', 'Shots on target, %',
        'Assists per 90', 'xA per 90', 'Shot assists per 90', 'Fouls per 90',
        'Possession in %',
    ]
    for col in cols:
        if col in data.columns:
            data[col] = _to_float(data[col])

    # ── derived stats ─────────────────────────────────────────────────────────
    data['xG per shot'] = data['xG'] / data['Shots']
    data['Finishing'] = data['Goals per 90'] - data['xG per 90']

    data['Key passes per pass'] = data['Key passes per 90'] / data['Passes per 90']
    data['Through passes per pass'] = data['Through passes per 90'] / data['Passes per 90']

    data['Successful dribbles per 90'] = data['Dribbles per 90'] * (data['Successful dribbles, %'] / 100)
    data['Successful dribbles per received pass'] = data['Successful dribbles per 90'] / data['Received passes per 90']

    data['Accurate crosses per 90'] = data['Crosses per 90'] * (data['Accurate crosses, %'] / 100)
    data['Accurate crosses per received pass'] = data['Accurate crosses per 90'] / data['Received passes per 90']

    data['Defensive duels won per 90'] = data['Defensive duels per 90'] * (data['Defensive duels won, %'] / 100)
    data['Aerial duels won per 90'] = data['Aerial duels per 90'] * (data['Aerial duels won, %'] / 100)

    data['Ball Progression (passing)'] = (
        (data['Progressive passes per 90'] + data['Forward passes per 90']) / data['Passes per 90']
    )

    data['Completed progressive passes per 90'] = (
        data['Progressive passes per 90'] * (data['Accurate progressive passes, %'] / 100)
    )
    data['Completed passes to final third per 90'] = (
        data['Passes to final third per 90'] * (data['Accurate passes to final third, %'] / 100)
    )
    data['Completed passes to penalty area per 90'] = (
        data['Passes to penalty area per 90'] * (data['Accurate passes to penalty area, %'] / 100)
    )

    data['Ball progression through passing'] = (
        data['Deep completions per 90']
        + data['Completed passes to penalty area per 90']
        + data['Completed passes to final third per 90']
        + data['Completed progressive passes per 90']
    )

    data['Passing accuracy (prog/1/3/forw)'] = (
        (data['Accurate forward passes, %'] + data['Accurate passes to final third, %'] + data['Accurate progressive passes, %']) / 3
    )

    data['Progressive runs per received pass'] = data['Progressive runs per 90'] / data['Received passes per 90']

    # ── possession-adjusted defensive stats ───────────────────────────────────
    data['Possession in dec'] = data['Possession in %'] / 100
    opp_poss = 1 - data['Possession in dec']
    data['PAdj Defensive duels won per 90'] = data['Defensive duels won per 90'] / opp_poss
    data['PAdj Aerial duels won per 90'] = data['Aerial duels won per 90'] / opp_poss
    data['PAdj Successful defensive actions per 90'] = data['Successful defensive actions per 90'] / opp_poss

    return data
