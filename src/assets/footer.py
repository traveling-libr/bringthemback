# Import dash libraries
from dash import html, dcc
import dash_bootstrap_components as dbc

# Import local libraries
import utils.style as bbs

footer = html.Footer(
    dbc.Container(
        [
            #html.Hr(),
            html.Br(),

            dbc.Row(dbc.Col(html.Div(dcc.Link("Donate to the ACLU", href="https://action.aclu.org/give/donate-to-aclu-multistep", target="_blank", style={'text-decoration':'none'}), style={'fontSize':'1.5em', 'textAlign':'center'}), width={'size': 12}), justify="center"),
            
            html.Br(),
        
            html.Br(),
        ]
    )
)