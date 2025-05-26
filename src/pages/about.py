# Import dash libraries
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Import local libraries
from utils.content import app_text
import utils.style as bbs

dash.register_page(__name__, name="About", path="/about", order=2)

layout = html.Div([
            dbc.Row(dbc.Col(html.Br())),

            dbc.Row(dbc.Col(html.Div(app_text['About'], id='about'
            ), width={'size': 11, 'offsetr': 1}
            ), justify="center"),

        dbc.Row(dbc.Col(html.Br())),
        dbc.Row(dbc.Col(html.Br()))
        
    ], style={'color':bbs.text_color, 'textAlign':'center'})
