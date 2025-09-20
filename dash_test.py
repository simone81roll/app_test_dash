import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# --- 1. PREPARAZIONE DEI DATI E STILI ---

# Dati dei clienti e degli ordini (dal tuo script originale)
data_clienti = {
    'ID_cliente': [1, 2, 3, 4, 5, 6, 7],
    'nome_cliente': ['Mario Rossi', 'Laura Bianchi', 'Giuseppe Verdi', 'Anna Neri', 'Paolo Forti', 'Silvia Gallo', 'Marco Bini'],
    'citta': ['Roma', 'Milano', 'Napoli', 'Torino', 'Bologna', 'Milano', 'Roma']
}
clienti = pd.DataFrame(data_clienti)

data_ordini = {
    'ID_ordine': [101, 102, 103, 104, 105, 106, 107, 108],
    'ID_cliente': [1, 3, 2, 1, 5, 6, 10, 4],
    'data_ordine': pd.to_datetime(['2024-01-15', '2024-01-17', '2024-02-01', '2024-02-05', '2024-02-10', '2024-03-01', '2024-03-05', '2024-03-10']),
    'Prodotto': ['Telecaster', 'Stratocaster', 'Les Paul', 'SG', 'Jazzmaster','Es-335','Gretsch White Falcon','Flying V'],
    'importo': [150.50, 200.00, 75.25, 300.00, 120.00, 80.00, 50.00, 250.00]
}
ordini = pd.DataFrame(data_ordini)

# Scegliamo un font da Google Fonts
external_stylesheets = ['https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap']

# Inizializziamo l'app con il nostro foglio di stile esterno
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True # Necessario per app multi-pagina

# Definiamo una palette di colori per un look moderno
COLORI = {
    'background': '#1E1E1E',
    'text': '#EAEAEA',
    'accent': '#00A3FF'
}

# --- 2. LAYOUT DELLE PAGINE ---

# Layout per la pagina Clienti (il nostro vecchio codice, migliorato)
def crea_pagina_clienti():
    return html.Div([
        html.H2('Anagrafica Clienti', style={'color': COLORI['accent']}),
        html.P('Usa i campi qui sotto per filtrare la tabella in tempo reale.'),
        html.Div([
            dcc.Input(id='filtro-nome', type='text', placeholder='Filtra per nome...',
                      style={'marginRight': '10px', 'padding': '5px'}),
            dcc.Input(id='filtro-citta', type='text', placeholder='Filtra per città...',
                      style={'padding': '5px'}),
        ], style={'marginBottom': '20px'}),
        dash_table.DataTable(
            id='tabella-clienti',
            columns=[{"name": i, "id": i} for i in clienti.columns],
            data=clienti.to_dict('records'),
            style_header={'backgroundColor': COLORI['accent'], 'color': 'black', 'fontWeight': 'bold'},
            style_data={'backgroundColor': '#333333', 'color': COLORI['text']},
            style_cell={'border': '1px solid #555555', 'padding': '10px', 'textAlign': 'left'},
        )
    ])

# Layout per la nuova pagina Ordini con un grafico
def crea_pagina_ordini():
    # Raggruppiamo i dati per prodotto
    vendite_prodotto = ordini.groupby('Prodotto')['importo'].sum().reset_index()
    # Creiamo il grafico a barre
    fig = px.bar(
        vendite_prodotto,
        x='Prodotto',
        y='importo',
        title='Totale Vendite per Prodotto',
        labels={'importo': 'Importo Totale (€)', 'Prodotto': 'Modello Chitarra'},
        template='plotly_dark' # Usiamo un template scuro
    )
    fig.update_layout(
        plot_bgcolor=COLORI['background'],
        paper_bgcolor=COLORI['background'],
        font_color=COLORI['text'],
        title_font_color=COLORI['accent']
    )
    return html.Div([
        html.H2('Analisi Ordini', style={'color': COLORI['accent']}),
        dcc.Graph(figure=fig)
    ])

# --- 3. LAYOUT PRINCIPALE DELL'APP ---

# Definiamo lo stile per la sidebar e il contenuto
STYLE_SIDEBAR = {
    'position': 'fixed', 'top': 0, 'left': 0, 'bottom': 0,
    'width': '20rem', 'padding': '2rem 1rem',
    'backgroundColor': '#111111'
}

STYLE_CONTENUTO = {
    'marginLeft': '22rem', 'padding': '2rem 1rem'
}

# Il layout principale contiene il menu e il contenitore per le pagine
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    
    # Sidebar di navigazione
    html.Div([
        html.H2("Dashboard", style={'color': 'white'}),
        html.Hr(style={'borderColor': '#444444'}),
        html.P("Naviga tra le sezioni:", style={'color': COLORI['text']}),
        html.Nav([
            dcc.Link('Clienti', href='/clienti', className='nav-link'),
            dcc.Link('Ordini', href='/ordini', className='nav-link'),
        ], style={'display': 'flex', 'flexDirection': 'column'}),
    ], style=STYLE_SIDEBAR),

    # Contenitore dove verranno caricate le pagine
    html.Div(id='page-content', style=STYLE_CONTENUTO)
], style={'fontFamily': 'Roboto, sans-serif', 'backgroundColor': COLORI['background'], 'color': COLORI['text'], 'minHeight': '100vh'})


# --- 4. CALLBACKS ---

# Callback per aggiornare il contenuto della pagina (il "router")
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/clienti':
        return crea_pagina_clienti()
    elif pathname == '/ordini':
        return crea_pagina_ordini()
    else:
        # Pagina di default o di benvenuto
        return html.Div([
            html.H1('Benvenuto!', style={'color': COLORI['accent']}),
            html.P('Seleziona una pagina dal menu a sinistra per iniziare.')
        ])

# Callback per la tabella interattiva della pagina Clienti
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

# --- 5. ESECUZIONE DELL'APP ---
if __name__ == '__main__':
    app.run(debug=True)