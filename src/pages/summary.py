# Import dash libraries
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Import local libraries
from utils.content import bar_init, bar_dict

stat_ = bar_init['stat']
age_ = bar_init['age']
rec_ = bar_init['rec']

stat_dropdown = html.Div(
    [
        html.Label("Select immigration status", htmlFor="slct_stat"),
        dcc.Dropdown(bar_dict['stat'], stat_, id='slct_stat'), 
        html.Div(id='stat_output_container', children=[]),
    ]
)

age_dropdown = html.Div(
    [
        html.Label("Select age group", htmlFor="slct_age"),
        dcc.Dropdown(bar_dict['age'], age_, id='slct_age'), 
        html.Div(id='age_output_container', children=[]),
    ]
)

rec_dropdown = html.Div(
    [
        html.Label("Select criminal record", htmlFor="slct_rec"),
        dcc.Dropdown(bar_dict['rec'], rec_, id='slct_rec'), 
        html.Div(id='rec_output_container', children=[]),
    ]
)

dash.register_page(__name__, name="Summary", order=5)

layout = html.Div([
    
    dbc.Row(dbc.Col(html.Br())),

    dbc.Row([dbc.Col(stat_dropdown, width={'size': 3, 'offsetr': 1}),
        dbc.Col(age_dropdown, width={'size': 3, 'offsetr': 1}),
        dbc.Col(rec_dropdown, width={'size': 3, 'offsetr': 1})], 
    justify="center"),

    dbc.Row(dbc.Col(dcc.Graph(
        id='bar_chart',
        figure={}
    ))),  
    dbc.Row(dbc.Col(html.Br())),
    dbc.Row(dbc.Col(html.Br()))
        #])
])

