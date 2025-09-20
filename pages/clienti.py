# File: pages/clienti.py

from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc

# Importa l'oggetto 'app' dal file app.py
from app import app 

# (Qui potresti caricare i dati da un file CSV o un database)
data_clienti = {
    'ID_cliente': [1, 2, 3, 4, 5, 6, 7],
    'nome_cliente': ['Mario Rossi', 'Laura Bianchi', 'Giuseppe Verdi', 'Anna Neri', 'Paolo Forti', 'Silvia Gallo', 'Marco Bini'],
    'citta': ['Roma', 'Milano', 'Napoli', 'Torino', 'Bologna', 'Milano', 'Roma']
}
clienti = pd.DataFrame(data_clienti)

# Definisci il layout della pagina
layout = html.Div([
    html.H2('Anagrafica Clienti', className='display-4'),
    html.P('Usa i campi qui sotto per filtrare la tabella.', className='lead'),
    html.Hr(),
    dbc.Row([
        dbc.Col(dcc.Input(id='filtro-nome', type='text', placeholder='Filtra per nome...'), width=4),
        dbc.Col(dcc.Input(id='filtro-citta', type='text', placeholder='Filtra per città...'), width=4),
    ], className='mb-3'),
    
    dash_table.DataTable(
        id='tabella-clienti',
        columns=[{"name": i, "id": i} for i in clienti.columns],
        data=clienti.to_dict('records'),
        # Ho aggiunto questi parametri di stile per rendere la tabella visibile
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold',
            'color': 'black'
        },
        style_data={
            'backgroundColor': 'white',
            'color': 'black'
        },
        style_cell={
            'textAlign': 'left'
        }
    )
])

# Definisci le callback specifiche di QUESTA pagina
@app.callback(
    Output('tabella-clienti', 'data'),
    Input('filtro-nome', 'value'),
    Input('filtro-citta', 'value')
)
def aggiorna_tabella_clienti(filtro_nome, filtro_citta):
    clienti_filtrati = clienti.copy()
    if filtro_nome:
        clienti_filtrati = clienti_filtrati[clienti_filtrati['nome_cliente'].str.contains(filtro_nome, case=False, na=False)]
    if filtro_citta:
        clienti_filtrati = clienti_filtrati[clienti_filtrati['citta'].str.contains(filtro_citta, case=False, na=False)]
    return clienti_filtrati.to_dict('records')
