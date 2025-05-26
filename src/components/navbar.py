# Import dash libraries
import dash
from dash import html, dcc

# Not sure what the href should be to get the pages in the pages folder
page_links = [dcc.Link(page['name'], href='/', className="nav-link")
            for page in dash.page_registry.values()]

navbar = html.Nav(children=[
            html.Div([
            html.Div(page_links, className="navbar-nav")
            ], className="container-fluid"),
        ], className="navbar navbar-expand-lg bg-dark", **{"data-bs-theme": "dark"}),
