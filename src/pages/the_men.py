# Import dash libraries
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Import local libraries
from utils.content import men_df, mid_init
import utils.style as bbs

names_dict = men_df.set_index('ID')['Reverse Name'].to_dict()

# Husbands, Fathers, Sons, Brothers, and Friends

dropdown_options = []
for k, v in names_dict.items():
    d = {}
    d['label'] = v
    d['value'] = k
    dropdown_options.append(d)

mid_ = mid_init

name_dropdown = html.Div(
    [
        html.Label("Select a name", htmlFor="slct_name"),
        dcc.Dropdown(dropdown_options, mid_, id='slct_name'), 
        html.Div(id='name_output_container', children=[]),
    ]
)

dash.register_page(__name__, name="The Men", path="/the_men", order=3)

layout = html.Div([
    dbc.Row(html.Br()),
    dbc.Row([
             dbc.Col(html.Div(id='name_text', children=[]), width={'size': 8, 'offsetr': 1}),
             dbc.Col(name_dropdown, width={'size': 3, 'offsetr': 1}),
], justify='center'),
dbc.Row([
             dbc.Col(html.Div(id='summary_text', children=[]), width={'size': 3, 'offsetr': 1}),
             dbc.Col(html.Div(id='account_text', children=[]), width={'size': 5}),
             dbc.Col(html.Div(), width={'size': 3, 'offsetr': 1}),
], justify='center'),


dbc.Row(dbc.Col(html.Br())),
dbc.Row(dbc.Col(html.Br()))
])

