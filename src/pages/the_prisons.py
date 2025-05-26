# Import general libraries
import pandas as pd

# Import dash libraries
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Import local libraries
from utils.content import loc_df, loc_list, map_init
import utils.style as bbs

loc_df = loc_df.rename(columns={'SourceID':'locID'}).copy()
loc_ = map_init['loc']
lat_ = map_init['lat']
lon_ = map_init['lon']

dash.register_page(__name__, name="The Prisons", path="/the_prisons", order=4)

layout = html.Div([
            dbc.Row(dbc.Col(html.Br())),

            dbc.Row(dbc.Col(html.H3(children='The El Salvador Prison System'), width={'size': 11, 'offsetr': 1}), justify="center"),

            dbc.Row(dbc.Col(html.Br())),

            dbc.Row(dbc.Col(dcc.RadioItems(id='slct_loc', options=loc_list, value=loc_, inline=True, style={'accent-color':bbs.accent_color}, inputStyle={"margin-left":"20px", "margin-right":"5px"}), width={'size': 11, 'offsetr': 1}), justify="center"),

            dbc.Row(dbc.Col(html.Div(id='loc_output_container', children=[]), style={"margin-left":"40px"}, width={'size': 11, 'offsetr': 1}), justify="center"),

            dbc.Row([dbc.Col(dcc.Graph(id='elsl_map', figure={}, config={'scrollZoom': True}), width={'size': 6, 'offsetr': 1}),
                dbc.Col(id='map_text', children=[], width={'size': 5, 'offsetr': 1})], justify="center"),
            
            dbc.Row(dbc.Col(html.Br())),
            dbc.Row(dbc.Col(html.Br()))

        ])