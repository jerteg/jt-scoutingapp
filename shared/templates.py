template_config = {
    "Right-Back": {
        "positions": ['RB','RWB'],
        "stats": [
            'xG per 90','xA per 90',
            'Accurate crosses per received pass', 'Accurate crosses, %',
            'Shot assists per 90',
            'Successful dribbles per received pass',
            'Progressive runs per received pass',
            'Ball progression through passing',
            'Passing accuracy (prog/1/3/forw)',
            'Defensive duels won per 90', 'Defensive duels won, %',
            'Aerial duels won per 90', 'Aerial duels won, %',
            'PAdj Interceptions'
        ],
        "label": "RB Template",
        "rotate_stats": [
            'xG per 90','xA per 90',
            'Accurate crosses per received pass', 'Accurate crosses, %',
            'Shot assists per 90',
            'Successful dribbles per received pass',
            'Progressive runs per received pass',
            'Ball progression through passing'
        ]
    },

    "Centre-Back": {
        "positions": ['CB', 'RCB', 'LCB'],
        "stats": [
             'Progressive runs per received pass', 
             'Ball progression through passing', 
             'Passing accuracy (prog/1/3/forw)',
             'Defensive duels won per 90', 
             'Defensive duels won, %',
             'Aerial duels won per 90', 
             'Aerial duels won, %', 
             'PAdj Interceptions',
             'Fouls per 90'
        ],
        "label": "CB Template",
        "negative_stats": ['Fouls per 90'],
        "rotate_stats": [
             'Progressive runs per received pass', 
             'Ball progression through passing', 
             'Completed progressive passes per 90',
             'Passing accuracy (prog/1/3/forw)', 
             'Defensive duels won per 90', 
             'Defensive duels won, %'
        ]
    },

    "Left-Back": {
        "positions": ['LB', 'LWB'],
        "stats": [
            'xG per 90','xA per 90',
            'Accurate crosses per received pass', 'Accurate crosses, %',
            'Shot assists per 90',
            'Successful dribbles per received pass',
            'Progressive runs per received pass',
            'Ball progression through passing',
            'Passing accuracy (prog/1/3/forw)',
            'Defensive duels won per 90', 'Defensive duels won, %',
            'Aerial duels won per 90', 'Aerial duels won, %',
            'PAdj Interceptions'
        ],
        "label": "LB Template",
        "rotate_stats": [
            'xG per 90','xA per 90',
            'Accurate crosses per received pass', 'Accurate crosses, %',
            'Shot assists per 90',
            'Successful dribbles per received pass',
            'Progressive runs per received pass',
            'Ball progression through passing'
        ]
    },
    
    "Defensive Midfielder": {
        "positions": ['RDMF','LDMF','DMF'],
        "stats": [
             'xA per 90', 
             'Successful dribbles, %',
             'Progressive runs per received pass', 
             'Ball progression through passing', 
             'Passing accuracy (prog/1/3/forw)', 
             'Defensive duels won per 90', 
             'Defensive duels won, %',
             'Aerial duels won per 90', 
             'Aerial duels won, %', 
             'Successful defensive actions per 90',
             'PAdj Interceptions',
             'Fouls per 90'
        ],
        "label": "DM Template",
        "negative_stats": ['Fouls per 90'],
        "rotate_stats": [
             'xA per 90', 
             'Successful dribbles, %',
             'Progressive runs per received pass', 
             'Ball progression through passing', 
             'Passing accuracy (prog/1/3/forw)', 
             'Defensive duels won per 90'
        ]
    },
    
    "Central Midfielder": {
        "positions": ['RDMF','LDMF','RCMF','LCMF'],
        "stats": [
            'xG per 90','Touches in box per 90','xA per 90',
            'Key passes per pass','Through passes per pass',
            'Successful dribbles per received pass',
            'Successful dribbles, %',
            'Progressive runs per received pass',
            'Ball progression through passing',
            'Passing accuracy (prog/1/3/forw)',
            'Defensive duels won per 90','Defensive duels won, %',
            'Aerial duels won per 90','Aerial duels won, %',
            'Successful defensive actions per 90',
            'PAdj Interceptions'
        ],
        "label": "CM Template",
        "rotate_stats": [
            "xG per 90","xA per 90","Touches in box per 90",
            "Key passes per pass","Through passes per pass",
            "Successful dribbles per received pass",
            "Ball progression through passing",
            "Successful dribbles, %",
            "Progressive runs per received pass"
        ]
    },

    "Attacking Midfielder": {
        "positions": ['RCMF','LCMF','AMF'],
        "stats": [
            'xG per 90',
            'xG per shot',
            'Finishing',
            'Touches in box per 90',
            'xA per 90', 
            'Key passes per pass', 
            'Through passes per pass', 
            'Successful dribbles per received pass',
            'Successful dribbles, %',
            'Progressive runs per received pass', 
            'Ball progression through passing', 
            'Passing accuracy (prog/1/3/forw)', 
            'Defensive duels won, %', 
            'Aerial duels won, %',
            'PAdj Interceptions'
        ],
        "label": "AM Template",
        "rotate_stats": [
            'xG per 90',
            'xG per shot',
            'Finishing',
            'Touches in box per 90',
            'xA per 90', 
            'Key passes per pass', 
            'Through passes per pass', 
            'Successful dribbles per received pass'
        ]
    },
    
    "Winger": {
        "positions": ['LWF','LAMF','LW','RWF','RAMF','RW'],
        "stats": [
            'Finishing','xG per 90','xG per shot',
            'Touches in box per 90','xA per 90',
            'Shot assists per 90','Key passes per pass',
            'Accurate crosses per received pass','Accurate crosses, %',
            'Successful dribbles per received pass',
            'Progressive runs per received pass',
            'Ball progression through passing',
            'Passing accuracy (prog/1/3/forw)',
            'Defensive duels won, %','Aerial duels won, %',
            'PAdj Interceptions'
        ],
        "label": "Winger Template",
        "rotate_stats": [
            'Non-penalty goals per 90','xG per 90','xG per shot',
            'Touches in box per 90','xA per 90',
            'Shot assists per 90','Key passes per pass',
            'Accurate crosses per received pass','Finishing', 'Accurate crosses, %'
        ]
    }, 

    "Striker": {
        "positions": ['CF'],
        "stats": [
             'xG per 90',
             'xG per shot',
             'Finishing',
             'Touches in box per 90',
             'xA per 90', 
             'Key passes per pass',  
             'Successful dribbles per received pass',
             'Successful dribbles, %',
             'Progressive runs per received pass', 
             'Passing accuracy (prog/1/3/forw)', 
             'Defensive duels won, %', 
             'Aerial duels won, %',
             'PAdj Interceptions'
        ],
        "label": "Striker Template",
        "rotate_stats": [
             'xG per 90',
             'xG per shot',
             'Finishing',
             'Touches in box per 90',
             'xA per 90', 
             'Key passes per pass',  
             'Successful dribbles per received pass'
        ]
    }
}

report_template = {

    "Goalscoring": {
        "stats": [
            "Non-penalty goals per 90",
            "xG per 90", 
            "xG per shot", 
            "Finishing", 
            "Shots per 90", 
            "Shots on target, %",
            "Touches in box per 90"
        ]
    },

    "Chance creation": {
        "stats": [
            "Assists per 90", 
            "xA per 90", 
            "Shot assists per 90", 
            "Key passes per pass", 
            "Through passes per pass",
            "Accurate crosses per received pass", 
            "Accurate crosses, %"
        ]
    },

    "Dribbling": {
        "stats": [
            "Successful dribbles per received pass", 
            "Successful dribbles, %", 
            "Progressive runs per received pass",
            "Fouls suffered per 90"
        ]
    },

    "Passing": {
        "stats": [
            "Completed progressive passes per 90", 
            "Accurate progressive passes, %",
            "Completed passes to final third per 90", 
            "Accurate passes to final third, %",
            "Completed passes to penalty area per 90", 
            "Accurate passes to penalty area, %", 
            "Deep completions per 90"
        ]
    },

    "Defending": {
        "stats": [
            "Defensive duels won per 90",
            "Defensive duels won, %",
            "Aerial duels won per 90",
            "Aerial duels won, %",
            "PAdj Interceptions",
            "Successful defensive actions per 90",
            "Fouls per 90"
            ],
        "negative_stats": ['Fouls per 90']
    }
}
        
position_groups = {
    "Right-Back": ['RB', 'RWB'],
    "Centre-Back": ['CB', 'RCB', 'LCB'],
    "Left-Back": ['LB', 'LWB'],
    "Defensive Midfielder": ['DMF', 'RDMF', 'LDMF'],
    "Central Midfielder": ['RDMF', 'LDMF', 'RCMF', 'LCMF'],
    "Attacking Midfielder": ['RCMF', 'LCMF', 'AMF'],
    "Winger": ['LW', 'RW', 'LWF', 'RWF', 'LAMF', 'RAMF'],
    "Striker": ['CF']
}

position_to_template = {
    "Right-Back": "Right-Back",
    "Centre-Back": "Centre-Back",
    "Left-Back": "Left-Back",
    "Defensive Midfielder": "Defensive Midfielder",
    "Central Midfielder": "Central Midfielder", 
    "Attacking Midfielder": "Attacking Midfielder", 
    "Winger": "Winger",
    "Striker": "Striker"
}

position_labels = {
    "Left Wing": ['LWF', 'LAMF', 'LW'],
    "Right Wing": ['RWF', 'RAMF', 'RW'],
    "Striker": ['CF'],
    "Right-Back": ['RB', 'RWB'],
    "Left-Back": ['LB', 'LWB'],
    "Centre-Back": ['CB', 'RCB', 'LCB'],
    "Central Midfielder": ['RDMF', 'RCMF', 'LDMF', 'LCMF'],
    "Attacking Midfielder": ['AMF'],
    "Defensive Midfielder": ['DMF']
}

position_map = {
    pos: label
    for label, positions in position_labels.items()
    for pos in positions
}