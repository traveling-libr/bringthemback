# Import dash libraries
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Import local libraries
from utils.content import references
import utils.style as bbs

refs = references['Reference'].tolist()
urls = references['URL'].tolist()
bibrefs = references['Bibliographic Reference'].tolist()

src_list = []
for i in range(0, len(refs)):
    src_list.append(html.P(["[", dcc.Link(refs[i], href=urls[i], target="_blank", style={'text-decoration':'none'}), "] ", bibrefs[i]]))

dash.register_page(__name__, name="Sources", path="/sources", order=6)

layout = html.Div([
    dbc.Row(dbc.Col(html.Br())),
    dbc.Row(dbc.Col(html.Div((src_list)), width={'size': 11, 'offsetr': 1}), justify="center"),
])
