# Import dash libraries
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Import local libraries
from utils.content import names_df, app_text
import utils.style as bbs

photo_ref_url = "https://www.cbsnews.com/news/photojournalist-witnesses-venezuelan-migrants-arrival-in-el-salvador-60-minutes/"

names = []
for n in names_df['Reverse Name'].tolist():
    names.append(html.P(n, style={'fontSize':'2em', 'textAlign':'center'}))

names_grp1 = []
for n in names_df.loc[names_df['Group']==1]['Reverse Name'].tolist():
    names_grp1.append(html.P(n, style={'fontSize':'2em', 'textAlign':'left'}))
names_grp2 = []
for n in names_df.loc[names_df['Group']==0]['Reverse Name'].tolist():
    names_grp2.append(html.P(n, style={'fontSize':'2em', 'textAlign':'left'}))

dash.register_page(__name__, name="Home", path='/', order=1)

layout = html.Div([
    html.Div([
        dbc.Row(dbc.Col(html.Br())),

        dbc.Row(dbc.Col(html.H1(children='Time in CECOT...', 
            style={'fontSize':'2em', 'textAlign':'center'}), 
            width={'size': 12})
            ),

        dbc.Row(dbc.Col(html.Br())),
    
        html.H1(id='time-counter', style={'fontSize':'4em', 'textAlign':'center', 'color':bbs.time_color, 'font-weight':'900'}),
        dbc.Row(dbc.Col(dcc.Interval(
            id='interval-component',
            interval=1000,  # Update every second (1000 ms)
            n_intervals=0
        ), width={'size': 8, 'offsetr': 2}), justify="center"),

        dbc.Row(dbc.Col(html.Br())),

        dbc.Row(dbc.Col(html.H1(children='Over 200 men imprisoned by Donald Trump.', 
            style={'fontSize':'2em', 'textAlign':'center'}), 
            width={'size': 12})
            ),
        dbc.Row(dbc.Col(html.H1(children='No due process.', 
            style={'color':bbs.emph_color, 'fontSize':'2em', 'textAlign':'center'}), 
            width={'size': 12})
            ),

        dbc.Row(dbc.Col(html.H1(children='Inhumane treatment.', 
            style={'color':bbs.emph_color, 'fontSize':'2em', 'textAlign':'center'}), 
            width={'size': 12})
            ),
        
        dbc.Row(dbc.Col(html.Br())),

        dbc.Row(dbc.Col(html.P(children=["CBS News published a photojournalist's video and photos of the men when they arrived at CECOT.",
            html.Br(),
            html.Span(dcc.Link("They had no idea what was coming.", href=photo_ref_url, target="_blank", style={'fontSize':'2em', 'text-decoration':'none'}))
            ], style={'fontSize':'1.5em', 'textAlign':'center'}
            ), width={'size': 10, 'offsetr': 2}
            ), justify="center"),

    ], style={'background-color':bbs.div_bg}),

        #html.Div([
        dbc.Row(dbc.Col(html.Br())),

        dbc.Row(dbc.Col(html.H1(children='Do not forget about them...', 
            style={'fontSize':'4em', 'textAlign':'center', 'font-weight':'900'}), 
            width={'size': 12})
            ),

        #dbc.Row(dbc.Col(html.Div(dcc.Link("Donate to the ACLU", href="https://action.aclu.org/give/donate-to-aclu-multistep", target="_blank", style={'text-decoration':'none'}), style={'fontSize':'1.5em'}), width={'size': 5}), justify="center"),

        dbc.Row([dbc.Col(names_grp1, width={'size': 5, 'offsetr': 2}),
                     #dbc.Col(width={'size': 1}),
                     dbc.Col(names_grp2, width={'size': 5})
            ], justify="center"),
        #], style={'background-color':bbs.div_bg}),

        dbc.Row(dbc.Col(html.Div(app_text['Home Names'], id='home_names'), width={'size': 5}), justify="center"),

        dbc.Row(dbc.Col(html.Br())),
], style={'textAlign':'center'})