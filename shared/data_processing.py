import pandas as pd

def preprocess_data(data):
    data = data.copy()

    data['xG'] = data['xG'].astype(str).str.replace(',', '.', regex=True)
    data['Shots'] = data['Shots'].astype(str).str.replace(',', '.', regex=True)
    data['xG'] = pd.to_numeric(data['xG'], errors='coerce')
    data['Shots'] = pd.to_numeric(data['Shots'], errors='coerce')
    data['xG'] = data['xG'].astype(float)
    data['Shots'] = data['Shots'].astype(float)
    data['xG per shot'] = data['xG'] / data['Shots']

    data['Goals per 90'] = data['Goals per 90'].astype(str).str.replace(',', '.', regex=True)
    data['xG per 90'] = data['xG per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Goals per 90'] = pd.to_numeric(data['Goals per 90'], errors='coerce')
    data['xG per 90'] = pd.to_numeric(data['xG per 90'], errors='coerce')
    data['Goals per 90'] = data['Goals per 90'].astype(float)
    data['xG per 90'] = data['xG per 90'].astype(float)
    data['Finishing'] = data['Goals per 90'] - data['xG per 90']

    data['Passes per 90'] = data['Passes per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Key passes per 90'] = data['Key passes per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Passes per 90'] = pd.to_numeric(data['Passes per 90'], errors='coerce')
    data['Key passes per 90'] = pd.to_numeric(data['Key passes per 90'], errors='coerce')
    data['Passes per 90'] = data['Passes per 90'].astype(float)
    data['Key passes per 90'] = data['Key passes per 90'].astype(float)
    data['Key passes per pass'] = data['Key passes per 90'] / data['Passes per 90']

    data['Passes per 90'] = data['Passes per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Through passes per 90'] = data['Through passes per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Passes per 90'] = pd.to_numeric(data['Passes per 90'], errors='coerce')
    data['Through passes per 90'] = pd.to_numeric(data['Through passes per 90'], errors='coerce')
    data['Passes per 90'] = data['Passes per 90'].astype(float)
    data['Through passes per 90'] = data['Through passes per 90'].astype(float)
    data['Through passes per pass'] = data['Through passes per 90'] / data['Passes per 90']

    data['Dribbles per 90'] = data['Dribbles per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Successful dribbles, %'] = data['Successful dribbles, %'].astype(str).str.replace(',', '.', regex=True)
    data['Dribbles per 90'] = pd.to_numeric(data['Dribbles per 90'], errors='coerce')
    data['Successful dribbles, %'] = pd.to_numeric(data['Successful dribbles, %'], errors='coerce')
    data['Dribbles per 90'] = data['Dribbles per 90'].astype(float)
    data['Successful dribbles, %'] = data['Successful dribbles, %'].astype(float)
    data['Successful dribbles per 90'] = data['Dribbles per 90'] * (data['Successful dribbles, %']/100)

    data['Successful dribbles per 90'] = data['Successful dribbles per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Received passes per 90'] = data['Received passes per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Successful dribbles per 90'] = pd.to_numeric(data['Successful dribbles per 90'], errors='coerce')
    data['Received passes per 90'] = pd.to_numeric(data['Received passes per 90'], errors='coerce')
    data['Successful dribbles per 90'] = data['Successful dribbles per 90'].astype(float)
    data['Received passes per 90'] = data['Received passes per 90'].astype(float)
    data['Successful dribbles per received pass'] = data['Successful dribbles per 90'] / data['Received passes per 90']

    data['Crosses per 90'] = data['Crosses per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Accurate crosses, %'] = data['Accurate crosses, %'].astype(str).str.replace(',', '.', regex=True)
    data['Crosses per 90'] = pd.to_numeric(data['Crosses per 90'], errors='coerce')
    data['Accurate crosses, %'] = pd.to_numeric(data['Accurate crosses, %'], errors='coerce')
    data['Crosses per 90'] = data['Crosses per 90'].astype(float)
    data['Accurate crosses, %'] = data['Accurate crosses, %'].astype(float)
    data['Accurate crosses per 90'] = data['Crosses per 90'] * (data['Accurate crosses, %']/100)

    data['Accurate crosses per 90'] = data['Accurate crosses per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Received passes per 90'] = data['Received passes per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Accurate crosses per 90'] = pd.to_numeric(data['Accurate crosses per 90'], errors='coerce')
    data['Received passes per 90'] = pd.to_numeric(data['Received passes per 90'], errors='coerce')
    data['Accurate crosses per 90'] = data['Accurate crosses per 90'].astype(float)
    data['Received passes per 90'] = data['Received passes per 90'].astype(float)
    data['Accurate crosses per received pass'] = data['Accurate crosses per 90'] / data['Received passes per 90']

    data['Defensive duels per 90'] = data['Defensive duels per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Defensive duels won, %'] = data['Defensive duels won, %'].astype(str).str.replace(',', '.', regex=True)
    data['Defensive duels per 90'] = pd.to_numeric(data['Defensive duels per 90'], errors='coerce')
    data['Defensive duels won, %'] = pd.to_numeric(data['Defensive duels won, %'], errors='coerce')
    data['Defensive duels per 90'] = data['Defensive duels per 90'].astype(float)
    data['Defensive duels won, %'] = data['Defensive duels won, %'].astype(float)
    data['Defensive duels won per 90'] = data['Defensive duels per 90'] * (data['Defensive duels won, %']/100)

    data['Aerial duels per 90'] = data['Aerial duels per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Aerial duels won, %'] = data['Aerial duels won, %'].astype(str).str.replace(',', '.', regex=True)
    data['Aerial duels per 90'] = pd.to_numeric(data['Aerial duels per 90'], errors='coerce')
    data['Aerial duels won, %'] = pd.to_numeric(data['Aerial duels won, %'], errors='coerce')
    data['Aerial duels per 90'] = data['Aerial duels per 90'].astype(float)
    data['Aerial duels won, %'] = data['Aerial duels won, %'].astype(float)
    data['Aerial duels won per 90'] = data['Aerial duels per 90'] * (data['Aerial duels won, %']/100)

    data['Progressive passes per 90'] = data['Progressive passes per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Forward passes per 90'] = data['Forward passes per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Passes per 90'] = data['Passes per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Progressive passes per 90'] = pd.to_numeric(data['Progressive passes per 90'], errors='coerce')
    data['Forward passes per 90'] = pd.to_numeric(data['Forward passes per 90'], errors='coerce')
    data['Passes per 90'] = pd.to_numeric(data['Passes per 90'], errors='coerce')
    data['Progressive passes per 90'] = data['Progressive passes per 90'].astype(float)
    data['Passes per 90'] = data['Passes per 90'].astype(float)
    data['Forward passes per 90'] = data['Forward passes per 90'].astype(float)
    data['Ball Progression (passing)'] = (data['Progressive passes per 90']+data['Forward passes per 90']) / data['Passes per 90']

    data['Progressive passes per 90'] = data['Progressive passes per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Accurate progressive passes, %'] = data['Accurate progressive passes, %'].astype(str).str.replace(',', '.', regex=True)
    data['Progressive passes per 90'] = pd.to_numeric(data['Progressive passes per 90'], errors='coerce')
    data['Accurate progressive passes, %'] = pd.to_numeric(data['Accurate progressive passes, %'], errors='coerce')
    data['Progressive passes per 90'] = data['Progressive passes per 90'].astype(float)
    data['Accurate progressive passes, %'] = data['Accurate progressive passes, %'].astype(float)
    data['Completed progressive passes per 90'] = (data['Progressive passes per 90'] * (data['Accurate progressive passes, %']/100))

    data['Passes to final third per 90'] = data['Passes to final third per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Accurate passes to final third, %'] = data['Accurate passes to final third, %'].astype(str).str.replace(',', '.', regex=True)
    data['Passes to final third per 90'] = pd.to_numeric(data['Passes to final third per 90'], errors='coerce')
    data['Accurate passes to final third, %'] = pd.to_numeric(data['Accurate passes to final third, %'], errors='coerce')
    data['Passes to final third per 90'] = data['Passes to final third per 90'].astype(float)
    data['Accurate passes to final third, %'] = data['Accurate passes to final third, %'].astype(float)
    data['Completed passes to final third per 90'] = (data['Passes to final third per 90'] * (data['Accurate passes to final third, %']/100))

    data['Passes to penalty area per 90'] = data['Passes to penalty area per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Accurate passes to penalty area, %'] = data['Accurate passes to penalty area, %'].astype(str).str.replace(',', '.', regex=True)
    data['Passes to penalty area per 90'] = pd.to_numeric(data['Passes to penalty area per 90'], errors='coerce')
    data['Accurate passes to penalty area, %'] = pd.to_numeric(data['Accurate passes to penalty area, %'], errors='coerce')
    data['Passes to penalty area per 90'] = data['Passes to penalty area per 90'].astype(float)
    data['Accurate passes to penalty area, %'] = data['Accurate passes to penalty area, %'].astype(float)
    data['Completed passes to penalty area per 90'] = (data['Passes to penalty area per 90'] * (data['Accurate passes to penalty area, %']/100))

    data['Deep completions per 90'] = data['Deep completions per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Deep completions per 90'] = pd.to_numeric(data['Deep completions per 90'], errors='coerce')
    data['Deep completions per 90'] = data['Deep completions per 90'].astype(float)
    
    data['Ball progression through passing'] = (data['Deep completions per 90'] + data['Completed passes to penalty area per 90'] + data['Completed passes to final third per 90'] + data['Completed progressive passes per 90'])

    data['Accurate forward passes, %'] = data['Accurate forward passes, %'].astype(str).str.replace(',', '.', regex=True)
    data['Accurate passes to final third, %'] = data['Accurate passes to final third, %'].astype(str).str.replace(',', '.', regex=True)
    data['Accurate progressive passes, %'] = data['Accurate progressive passes, %'].astype(str).str.replace(',', '.', regex=True)
    data['Accurate forward passes, %'] = pd.to_numeric(data['Accurate forward passes, %'], errors='coerce')
    data['Accurate passes to final third, %'] = pd.to_numeric(data['Accurate passes to final third, %'], errors='coerce')
    data['Accurate progressive passes, %'] = pd.to_numeric(data['Accurate progressive passes, %'], errors='coerce')
    data['Accurate forward passes, %'] = data['Accurate forward passes, %'].astype(float)
    data['Accurate passes to final third, %'] = data['Accurate passes to final third, %'].astype(float)
    data['Accurate progressive passes, %'] = data['Accurate progressive passes, %'].astype(float)
    data['Passing accuracy (prog/1/3/forw)'] = (data['Accurate forward passes, %']+data['Accurate passes to final third, %']+data['Accurate progressive passes, %'])/3

    data['Received passes per 90'] = data['Received passes per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Progressive runs per 90'] = data['Progressive runs per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Received passes per 90'] = pd.to_numeric(data['Received passes per 90'], errors='coerce')
    data['Progressive runs per 90'] = pd.to_numeric(data['Progressive runs per 90'], errors='coerce')
    data['Received passes per 90'] = data['Received passes per 90'].astype(float)
    data['Progressive runs per 90'] = data['Progressive runs per 90'].astype(float)
    data['Progressive runs per received pass'] = data['Progressive runs per 90'] / data['Received passes per 90']

    data['Successful defensive actions per 90'] = data['Successful defensive actions per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Successful defensive actions per 90'] = pd.to_numeric(data['Successful defensive actions per 90'], errors='coerce')

    data['PAdj Interceptions'] = data['PAdj Interceptions'].astype(str).str.replace(',', '.', regex=True)
    data['PAdj Interceptions'] = pd.to_numeric(data['PAdj Interceptions'], errors='coerce')

    data['Touches in box per 90'] = data['Touches in box per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Touches in box per 90'] = pd.to_numeric(data['Touches in box per 90'], errors='coerce')

    data['Fouls suffered per 90'] = data['Fouls suffered per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Fouls suffered per 90'] = pd.to_numeric(data['Fouls suffered per 90'], errors='coerce')

    data['Non-penalty goals per 90'] = data['Non-penalty goals per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Non-penalty goals per 90'] = pd.to_numeric(data['Non-penalty goals per 90'], errors='coerce')

    data['Shots per 90'] = data['Shots per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Shots per 90'] = pd.to_numeric(data['Shots per 90'], errors='coerce')

    data['Shots on target, %'] = data['Shots on target, %'].astype(str).str.replace(',', '.', regex=True)
    data['Shots on target, %'] = pd.to_numeric(data['Shots on target, %'], errors='coerce')

    data['Assists per 90'] = data['Assists per 90'].astype(str).str.replace(',', '.', regex=True)
    data['Assists per 90'] = pd.to_numeric(data['Assists per 90'], errors='coerce')


    
    return data
