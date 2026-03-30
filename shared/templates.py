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
        ],
        "weights": {
            "Non-penalty goals per 90": 0.20,
            "xG per 90": 0.20, 
            "xG per shot": 0.20, 
            "Finishing": 0.25, 
            "Shots per 90": 0.05, 
            "Shots on target, %": 0.05,
            "Touches in box per 90": 0.05
        }
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
        ],
        "weights": {
            "Assists per 90": 0.2, 
            "xA per 90": 0.3, 
            "Shot assists per 90": 0.2, 
            "Key passes per pass": 0.1, 
            "Through passes per pass": 0.1,
            "Accurate crosses per received pass": 0.05, 
            "Accurate crosses, %": 0.05
        }
    },

    "Dribbling": {
        "stats": [
            "Successful dribbles per received pass", 
            "Successful dribbles, %", 
            "Progressive runs per received pass"
        ],
        "weights": {
            "Successful dribbles per received pass": 0.3, 
            "Successful dribbles, %": 0.4, 
            "Progressive runs per received pass": 0.3
        }
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
        ],
        "weights": {
            "Completed progressive passes per 90": 0.15, 
            "Accurate progressive passes, %": 0.15,
            "Completed passes to final third per 90": 0.15, 
            "Accurate passes to final third, %": 0.15,
            "Completed passes to penalty area per 90": 0.15, 
            "Accurate passes to penalty area, %": 0.15, 
            "Deep completions per 90": 0.1
        }
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
        "negative_stats": ['Fouls per 90'],
        "weights": {
            "Defensive duels won per 90": 0.15,
            "Defensive duels won, %": 0.25,
            "Aerial duels won per 90": 0.15,
            "Aerial duels won, %": 0.25,
            "PAdj Interceptions": 0.1,
            "Successful defensive actions per 90": 0.05,
            "Fouls per 90": 0.05
        }
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

position_category_weights = {

    "Striker": {
        "Goalscoring": 0.5,
        "Chance creation": 0.2,
        "Dribbling": 0.15,
        "Passing": 0.1,
        "Defending": 0.05
    },

    "Winger": {
        "Goalscoring": 0.3,
        "Chance creation": 0.3,
        "Dribbling": 0.2,
        "Passing": 0.15,
        "Defending": 0.05
    },

    "Attacking Midfielder": {
        "Goalscoring": 0.2,
        "Chance creation": 0.3,
        "Dribbling": 0.2,
        "Passing": 0.2,
        "Defending": 0.1
    },

    "Central Midfielder": {
        "Goalscoring": 0.15,
        "Chance creation": 0.25,
        "Dribbling": 0.20,
        "Passing": 0.25,
        "Defending": 0.15
    },

    "Defensive Midfielder": {
        "Goalscoring": 0.05,
        "Chance creation": 0.1,
        "Dribbling": 0.15,
        "Passing": 0.35,
        "Defending": 0.35
    },

    "Centre-Back": {
        "Goalscoring": 0.05,
        "Chance creation": 0.05,
        "Dribbling": 0.05,
        "Passing": 0.35,
        "Defending": 0.5
    },

    "Right-Back": {
        "Goalscoring": 0.05,
        "Chance creation": 0.25,
        "Dribbling": 0.15,
        "Passing": 0.25,
        "Defending": 0.3
    },

    "Left-Back": {
        "Goalscoring": 0.05,
        "Chance creation": 0.25,
        "Dribbling": 0.15,
        "Passing": 0.25,
        "Defending": 0.3
    }
}
