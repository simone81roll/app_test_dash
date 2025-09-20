# File: app.py

import dash
import dash_bootstrap_components as dbc

# Usa un tema Bootstrap pre-costruito per uno stile pulito.
# Puoi trovare altri temi qui: https://bootswatch.com/
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.DARKLY],
                suppress_callback_exceptions=True
               )

server = app.server