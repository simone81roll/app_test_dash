# File: index.py

from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc


# Importa l'app e le pagine
from app import app, server # Importa anche server per il deployment
from pages import clienti, ordini

# Definisci la barra di navigazione in alto
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Clienti", href="/clienti")),
        dbc.NavItem(dbc.NavLink("Ordini", href="/ordini")),
    ],
    brand="Dashboard Aziendale",
    brand_href="/",
    color="primary",
    dark=True,
    className="mb-4" # Margine inferiore
)

# Layout principale dell'applicazione
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    # Contenitore dove verrà renderizzato il contenuto delle pagine
    dbc.Container(id='page-content') 
])

# Callback "Router" per cambiare le pagine
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/clienti':
        return clienti.layout
    elif pathname == '/ordini':
        return ordini.layout
    else:
        # Pagina di default - Ho aggiornato il codice qui!
        return dbc.Container([
            html.H1("Benvenuto!", className="display-3"),
            html.P("Seleziona una delle pagine dalla barra di navigazione per iniziare.", className="lead"),
        ], className="my-5") # my-5 è un margine sopra e sotto, per dare spazio

# Punto di avvio dell'applicazione
if __name__ == '__main__':
    app.run(debug=True)