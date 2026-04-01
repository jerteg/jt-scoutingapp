import pandas as pd

# ── Template configs per position group ───────────────────────────────────────

template_config = {
    "Right-Back": {
        "positions": ['RB', 'RWB'],
        "stats": [
            'xG per 90', 'xA per 90',
            'Accurate crosses per received pass', 'Accurate crosses, %',
            'Shot assists per 90',
            'Successful dribbles per received pass',
            'Progressive runs per received pass',
            'Ball progression through passing',
            'Passing accuracy (prog/1/3/forw)',
            'PAdj Defensive duels won per 90', 'Defensive duels won, %',
            'PAdj Aerial duels won per 90', 'Aerial duels won, %',
            'PAdj Interceptions'
        ],
        "label": "RB Template",
    },
    "Centre-Back": {
        "positions": ['CB', 'RCB', 'LCB'],
        "stats": [
            'Progressive runs per received pass',
            'Ball progression through passing',
            'Passing accuracy (prog/1/3/forw)',
            'PAdj Defensive duels won per 90', 'Defensive duels won, %',
            'PAdj Aerial duels won per 90', 'Aerial duels won, %',
            'PAdj Interceptions',
            'Fouls per 90'
        ],
        "label": "CB Template",
        "negative_stats": ['Fouls per 90'],
    },
    "Left-Back": {
        "positions": ['LB', 'LWB'],
        "stats": [
            'xG per 90', 'xA per 90',
            'Accurate crosses per received pass', 'Accurate crosses, %',
            'Shot assists per 90',
            'Successful dribbles per received pass',
            'Progressive runs per received pass',
            'Ball progression through passing',
            'Passing accuracy (prog/1/3/forw)',
            'PAdj Defensive duels won per 90', 'Defensive duels won, %',
            'PAdj Aerial duels won per 90', 'Aerial duels won, %',
            'PAdj Interceptions'
        ],
        "label": "LB Template",
    },
    "Defensive Midfielder": {
        "positions": ['RDMF', 'LDMF', 'DMF'],
        "stats": [
            'xA per 90',
            'Successful dribbles, %',
            'Progressive runs per received pass',
            'Ball progression through passing',
            'Passing accuracy (prog/1/3/forw)',
            'PAdj Defensive duels won per 90', 'Defensive duels won, %',
            'PAdj Aerial duels won per 90', 'Aerial duels won, %',
            'PAdj Successful defensive actions per 90',
            'PAdj Interceptions',
            'Fouls per 90'
        ],
        "label": "DM Template",
        "negative_stats": ['Fouls per 90'],
    },
    "Central Midfielder": {
        "positions": ['RDMF', 'LDMF', 'RCMF', 'LCMF'],
        "stats": [
            'xG per 90', 'Touches in box per 90', 'xA per 90',
            'Key passes per pass', 'Through passes per pass',
            'Successful dribbles per received pass', 'Successful dribbles, %',
            'Progressive runs per received pass',
            'Ball progression through passing',
            'Passing accuracy (prog/1/3/forw)',
            'PAdj Defensive duels won per 90', 'Defensive duels won, %',
            'PAdj Aerial duels won per 90', 'Aerial duels won, %',
            'PAdj Successful defensive actions per 90',
            'PAdj Interceptions'
        ],
        "label": "CM Template",
    },
    "Attacking Midfielder": {
        "positions": ['RCMF', 'LCMF', 'AMF'],
        "stats": [
            'xG per 90', 'xG per shot', 'Finishing',
            'Touches in box per 90', 'xA per 90',
            'Key passes per pass', 'Through passes per pass',
            'Successful dribbles per received pass', 'Successful dribbles, %',
            'Progressive runs per received pass',
            'Ball progression through passing',
            'Passing accuracy (prog/1/3/forw)',
            'Defensive duels won, %', 'Aerial duels won, %',
            'PAdj Interceptions'
        ],
        "label": "AM Template",
    },
    "Winger": {
        "positions": ['LWF', 'LAMF', 'LW', 'RWF', 'RAMF', 'RW'],
        "stats": [
            'Finishing', 'xG per 90', 'xG per shot',
            'Touches in box per 90', 'xA per 90',
            'Shot assists per 90', 'Key passes per pass',
            'Accurate crosses per received pass', 'Accurate crosses, %',
            'Successful dribbles per received pass',
            'Progressive runs per received pass',
            'Ball progression through passing',
            'Passing accuracy (prog/1/3/forw)',
            'Defensive duels won, %', 'Aerial duels won, %',
            'PAdj Interceptions'
        ],
        "label": "Winger Template",
    },
    "Striker": {
        "positions": ['CF'],
        "stats": [
            'xG per 90', 'xG per shot', 'Finishing',
            'Touches in box per 90', 'xA per 90',
            'Key passes per pass',
            'Successful dribbles per received pass', 'Successful dribbles, %',
            'Progressive runs per received pass',
            'Passing accuracy (prog/1/3/forw)',
            'Defensive duels won, %', 'Aerial duels won, %',
            'PAdj Interceptions'
        ],
        "label": "Striker Template",
    },
}

# ── Roles per position group ───────────────────────────────────────────────────

role_config = {
    "Right-Back": {
        "Defensive Full-Back": {
            "description": "Defensive-minded full-back focused on stopping direct opponent",
            "stats": {
                'PAdj Defensive duels won per 90': 0.150,
                'Defensive duels won, %':          0.175,
                'PAdj Aerial duels won per 90':    0.150,
                'Aerial duels won, %':             0.175,
                'PAdj Interceptions':              0.150,
                'Completed progressive passes per 90': 0.100,
                'Progressive runs per received pass':  0.100,
            },
        },
        "Attacking Full-Back": {
            "description": "Attacking-minded full-back focused on contributing to the attacking play",
            "stats": {
                'Defensive duels won, %':              0.100,
                'Aerial duels won, %':                 0.100,
                'Completed progressive passes per 90': 0.175,
                'Progressive runs per received pass':  0.175,
                'xA per 90':                           0.200,
                'Accurate crosses per received pass':  0.125,
                'Deep completions per 90':             0.125,
            },
        },
    },
    "Left-Back": {
        "Defensive Full-Back": {
            "description": "Defensive-minded full-back focused on stopping direct opponent",
            "stats": {
                'PAdj Defensive duels won per 90': 0.150,
                'Defensive duels won, %':          0.175,
                'PAdj Aerial duels won per 90':    0.150,
                'Aerial duels won, %':             0.175,
                'PAdj Interceptions':              0.150,
                'Completed progressive passes per 90': 0.100,
                'Progressive runs per received pass':  0.100,
            },
        },
        "Attacking Full-Back": {
            "description": "Attacking-minded full-back focused on contributing to the attacking play",
            "stats": {
                'Defensive duels won, %':              0.100,
                'Aerial duels won, %':                 0.100,
                'Completed progressive passes per 90': 0.175,
                'Progressive runs per received pass':  0.175,
                'xA per 90':                           0.200,
                'Accurate crosses per received pass':  0.125,
                'Deep completions per 90':             0.125,
            },
        },
    },
    "Centre-Back": {
        "Ball-Playing CB": {
            "description": "Centre-back focused on playing out from the back",
            "stats": {
                'Defensive duels won, %':                  0.125,
                'Aerial duels won, %':                     0.125,
                'Completed progressive passes per 90':     0.250,
                'Completed passes to final third per 90':  0.250,
                'Progressive runs per received pass':      0.100,
                'Accurate progressive passes, %':          0.075,
                'Accurate passes to final third, %':       0.075,
            },
        },
        "Sweeper": {
            "description": "Centre-back focused on winning duels in and around the box",
            "stats": {
                'PAdj Defensive duels won per 90': 0.200,
                'Defensive duels won, %':          0.200,
                'PAdj Aerial duels won per 90':    0.200,
                'Aerial duels won, %':             0.200,
                'PAdj Interceptions':              0.200,
            },
        },
    },
    "Defensive Midfielder": {
        "Ball-Winning Midfielder": {
            "description": "Defensive midfielder focused on intercepting the ball and winning duels",
            "stats": {
                'PAdj Defensive duels won per 90':         0.125,
                'Defensive duels won, %':                  0.125,
                'PAdj Aerial duels won per 90':            0.125,
                'Aerial duels won, %':                     0.125,
                'PAdj Interceptions':                      0.250,
                'Completed progressive passes per 90':     0.125,
                'Completed passes to final third per 90':  0.125,
            },
        },
        "Deep-Lying Playmaker": {
            "description": "Defensive midfielder focused on progressing play",
            "stats": {
                'Defensive duels won, %':                  0.125,
                'Aerial duels won, %':                     0.125,
                'Completed progressive passes per 90':     0.250,
                'Completed passes to final third per 90':  0.250,
                'Progressive runs per received pass':      0.100,
                'Accurate progressive passes, %':          0.075,
                'Accurate passes to final third, %':       0.075,
            },
        },
    },
    "Central Midfielder": {
        "Advanced Playmaker": {
            "description": "Central midfielder focused on creating opportunities",
            "stats": {
                'xG per 90':                           0.100,
                'xA per 90':                           0.250,
                'Successful dribbles, %':              0.250,
                'Completed passes to penalty area per 90': 0.100,
                'Key passes per pass':                 0.200,
                'Through passes per pass':             0.100,
            },
        },
        "Deep-Lying Playmaker": {
            "description": "Central midfielder focused on progressing play",
            "stats": {
                'Defensive duels won, %':                  0.125,
                'Aerial duels won, %':                     0.125,
                'Completed progressive passes per 90':     0.250,
                'Completed passes to final third per 90':  0.250,
                'Progressive runs per received pass':      0.100,
                'Accurate progressive passes, %':          0.075,
                'Accurate passes to final third, %':       0.075,
            },
        },
        "Box-to-Box Midfielder": {
            "description": "All-action central midfielder",
            "stats": {
                'PAdj Defensive duels won per 90':         0.125,
                'PAdj Aerial duels won per 90':            0.125,
                'PAdj Interceptions':                      0.125,
                'Completed progressive passes per 90':     0.125,
                'Completed passes to final third per 90':  0.125,
                'Progressive runs per received pass':      0.125,
                'xG per 90':                               0.125,
                'xA per 90':                               0.125,
            },
        },
        "Ball-Winning Midfielder": {
            "description": "Central midfielder focused on intercepting the ball and winning duels",
            "stats": {
                'PAdj Defensive duels won per 90':         0.125,
                'Defensive duels won, %':                  0.125,
                'PAdj Aerial duels won per 90':            0.125,
                'Aerial duels won, %':                     0.125,
                'PAdj Interceptions':                      0.250,
                'Completed progressive passes per 90':     0.125,
                'Completed passes to final third per 90':  0.125,
            },
        },
    },
    "Attacking Midfielder": {
        "Advanced Playmaker": {
            "description": "Attacking midfielder focused on creating opportunities",
            "stats": {
                'xG per 90':                               0.100,
                'xA per 90':                               0.250,
                'Successful dribbles, %':                  0.250,
                'Completed passes to penalty area per 90': 0.100,
                'Key passes per pass':                     0.200,
                'Through passes per pass':                 0.100,
            },
        },
        "Box Crasher": {
            "description": "Attacking midfielder focused on getting into the box and scoring",
            "stats": {
                'xG per 90':            0.200,
                'xG per shot':          0.300,
                'Finishing':            0.300,
                'Touches in box per 90': 0.150,
                'xA per 90':            0.050,
            },
        },
    },
    "Winger": {
        "Goalscoring Winger": {
            "description": "Winger focused on getting into the box and scoring",
            "stats": {
                'xG per 90':             0.200,
                'xG per shot':           0.300,
                'Finishing':             0.300,
                'Touches in box per 90': 0.150,
                'xA per 90':             0.050,
            },
        },
        "Creative Winger": {
            "description": "Winger focused on creating opportunities",
            "stats": {
                'xG per 90':                               0.100,
                'xA per 90':                               0.250,
                'Successful dribbles, %':                  0.250,
                'Completed passes to penalty area per 90': 0.100,
                'Key passes per pass':                     0.200,
                'Through passes per pass':                 0.100,
            },
        },
        "Direct Winger": {
            "description": "Winger focused on taking on opponents",
            "stats": {
                'Progressive runs per received pass':     0.250,
                'Successful dribbles per received pass':  0.250,
                'Successful dribbles, %':                 0.100,
                'xG per 90':                              0.150,
                'xA per 90':                              0.150,
                'Accurate crosses per received pass':     0.100,
            },
        },
    },
    "Striker": {
        "Poacher": {
            "description": "Striker focused on scoring goals only",
            "stats": {
                'xG per 90':             0.200,
                'xG per shot':           0.250,
                'Finishing':             0.400,
                'Touches in box per 90': 0.150,
            },
        },
        "Target Man": {
            "description": "Striker focused on holding up play and scoring goals",
            "stats": {
                'xG per 90':                    0.100,
                'xG per shot':                  0.150,
                'Finishing':                    0.150,
                'PAdj Aerial duels won per 90': 0.200,
                'Aerial duels won, %':          0.200,
                'xA per 90':                    0.100,
                'Touches in box per 90':        0.100,
            },
        },
        "Deep-Lying Forward": {
            "description": "Striker focused on contributing on the ball and scoring goals",
            "stats": {
                'xG per 90':                         0.150,
                'xG per shot':                       0.150,
                'Finishing':                         0.150,
                'xA per 90':                         0.250,
                'Key passes per pass':               0.200,
                'Successful dribbles per received pass': 0.100,
            },
        },
    },
}

# ── Position groups & mappings ────────────────────────────────────────────────

position_groups = {
    "Right-Back":           ['RB', 'RWB'],
    "Centre-Back":          ['CB', 'RCB', 'LCB'],
    "Left-Back":            ['LB', 'LWB'],
    "Defensive Midfielder": ['DMF', 'RDMF', 'LDMF'],
    "Central Midfielder":   ['RDMF', 'LDMF', 'RCMF', 'LCMF'],
    "Attacking Midfielder": ['RCMF', 'LCMF', 'AMF'],
    "Winger":               ['LW', 'RW', 'LWF', 'RWF', 'LAMF', 'RAMF'],
    "Striker":              ['CF'],
}

position_to_template = {pg: pg for pg in position_groups}

position_labels = {
    "Left Wing":            ['LWF', 'LAMF', 'LW'],
    "Right Wing":           ['RWF', 'RAMF', 'RW'],
    "Striker":              ['CF'],
    "Right-Back":           ['RB', 'RWB'],
    "Left-Back":            ['LB', 'LWB'],
    "Centre-Back":          ['CB', 'RCB', 'LCB'],
    "Central Midfielder":   ['RDMF', 'RCMF', 'LDMF', 'LCMF'],
    "Attacking Midfielder": ['AMF'],
    "Defensive Midfielder": ['DMF'],
}

position_map = {
    pos: label
    for label, positions in position_labels.items()
    for pos in positions
}

# ── League multipliers ────────────────────────────────────────────────────────

TOP5_LEAGUES = {"Premier League", "La Liga", "Italian Serie A", "Bundesliga", "Ligue 1"}

NEXT14_LEAGUES = {
    "Pro League", "Primeira Liga", "Liga Profesional", "Serie A BRA",
    "Championship", "Superligaen", "Ekstraklasa", "MLS", "Prva HNL",
    "Eliteserien", "Super Lig", "Eredivisie", "Liga Pro", "Swiss Super League",
    "Segunda Division",
}

LEAGUE_MULTIPLIERS_ALL = {
    "Premier League":     1.000,
    "La Liga":            0.949,
    "Italian Serie A":    0.936,
    "Bundesliga":         0.935,
    "Ligue 1":            0.926,
    "Pro League":         0.884,
    "Primeira Liga":      0.881,
    "Liga Profesional":   0.881,
    "Serie A BRA":        0.878,
    "Championship":       0.877,
    "Superligaen":        0.868,
    "Ekstraklasa":        0.860,
    "MLS":                0.858,
    "Prva HNL":           0.857,
    "Eliteserien":        0.855,
    "Super Lig":          0.850,
    "Eredivisie":         0.850,
    "Liga Pro":           0.849,
    "Segunda Division":   0.847,
    "Swiss Super League": 0.836,
}

LEAGUE_MULTIPLIERS_NEXT14 = {
    "Pro League":         1.000,
    "Primeira Liga":      0.996,
    "Liga Profesional":   0.996,
    "Serie A BRA":        0.993,
    "Championship":       0.991,
    "Superligaen":        0.981,
    "Ekstraklasa":        0.973,
    "MLS":                0.970,
    "Prva HNL":           0.969,
    "Eliteserien":        0.966,
    "Super Lig":          0.961,
    "Eredivisie":         0.961,
    "Liga Pro":           0.960,
    "Segunda Division":   0.958,
    "Swiss Super League": 0.945,
}
