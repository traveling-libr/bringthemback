# Import general libraries
import numpy as np
import pandas as pd
from datetime import datetime as dt

# Import dash libraries
import dash
from dash import html, dcc
from dash.dependencies import Input, Output

#import plotly libraries
import plotly.express as px

# Import local libraries
from utils.content import men_df, men_acct_df, map_content_df, loc_df, map_init
import utils.style as bbs
from utils.functions import get_accounts
from components import footer, navbar

#app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.JOURNAL])
app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True)

page_links = [dcc.Link(page['name'], href=page['relative_path'], className="nav-link")
            for page in dash.page_registry.values()]

app.layout = html.Div(
    [
        # main app framework
        html.Div("Cruel. Unusual. Indefensible.", style={'fontSize':'6em', 'textAlign':'center', 'background-color':bbs.title_bg, 'font-weight':'900'}),
        
        #html.Div(navbar),
        html.Nav(children=[
            html.Div([
            html.Div(page_links, className="navbar-nav")
            ], className="container-fluid"),
        ], className="navbar navbar-expand-lg bg-dark", **{"data-bs-theme": "dark"}),


        # content of each page
        dash.page_container,

        # footer
        html.Div(footer, style={'background-color':bbs.footer_bg})
    ]
)

# CALLBACKS

# Define callback for accounts of the men (About the Men)
@app.callback(
    [Output(component_id='name_output_container', component_property='children'),
     Output(component_id='name_text', component_property='children'),
     Output(component_id='summary_text', component_property='children'),
     Output(component_id='account_text', component_property='children')],
    [Input(component_id='slct_name', component_property='value')]
)
def get_report(name_slctd):

    mid_ = name_slctd

    dff1 = men_df.loc[men_df['ID']==mid_].copy()
    dff2 = men_acct_df.loc[men_acct_df['EID']==mid_].copy()

    name_ = dff1['Full Name'].values[0]
    container = "Selected name: {}".format(name_)

    name = dff1['Full Name'].values[0]
    age = dff1['Age at Deportation'].values[0]
    assign = dff1['Immigration Assignment'].values[0]
    status = dff1['Immigration Status'].values[0]
    record = dff1['Criminal Record'].values[0]
    sources = dff1['Reference_lnkd'].values[0]

    name_text = html.H3(name)
    
    summary_text = []
    summary_text.append(html.P([html.Span("Age", style={'color':bbs.emph_color, 'fontWeight':'900'}),
            html.Span(" (March 2025)", style={'color':bbs.text_color}),
	        html.Br(), html.Span(age, style={'color':bbs.text_color})]))
    summary_text.append(html.P([html.Span("Immigration Assignment and Status", style={'color':bbs.emph_color, 'fontWeight':'900'}),
	        html.Br(), html.Span(assign, style={'color':bbs.text_color}), html.Span("; "), html.Span(status, style={'color':bbs.text_color})]))
    summary_text.append(html.P([html.Span("Criminal Record", style={'color':bbs.emph_color, 'fontWeight':'900'}),
	        html.Br(), html.Span(record, style={'color':bbs.text_color})]))
    summary_text.append(html.P([html.Span("Sources", style={'color':bbs.emph_color, 'fontWeight':'900'}),
	        html.Br(), html.Span(sources, style={'color':bbs.text_color})]))

    summary_text = html.Div(summary_text, style={'fontSize':'1em', 'color':bbs.emph_color, 'textAlign':'left'})

    account_text = ''
    account_dict = get_accounts(dff2, rtype='dict')

    for k, v in account_dict.items():
        account_text = []
        account_text.append(html.P(k, style={'fontWeight':900, 'color':bbs.emph_color}))
        account_text.append(html.P(v))

    return container, name_text, summary_text, account_text

# Define callback for bar chart summary
@app.callback(
    [Output(component_id='stat_output_container', component_property='children'),
    Output(component_id='age_output_container', component_property='children'),
    Output(component_id='rec_output_container', component_property='children'),
     Output(component_id='bar_chart', component_property='figure')],
    [Input(component_id='slct_stat', component_property='value'),
     Input(component_id='slct_age', component_property='value'),
     Input(component_id='slct_rec', component_property='value')]
)
def get_summary(stat_slctd, age_slctd, rec_slctd):

    stat_cntr = "Selected immigration status: {}".format(stat_slctd)
    age_cntr = "Selected age: {}".format(age_slctd)
    rec_cntr = "Selected criminal record type: {}".format(rec_slctd)

    dff_init = pd.DataFrame()

    if stat_slctd == 'All':
        dff_init = men_df.copy()
    else:
        dff_init = men_df.loc[men_df['Immigration Status']==stat_slctd].copy()
    
    if age_slctd == 'All':
        dff_init2 = dff_init.copy()
    else:
        dff_init2 = dff_init.loc[dff_init['Age Group']==age_slctd].copy()
    
    if rec_slctd == 'All':
        dff = dff_init2.copy()
    else:
        dff = dff_init2.loc[dff_init2['Criminal Record']==rec_slctd].copy()

    summ = dff.groupby(['Immigration Assignment']).aggregate(cnt=('ID', 'count')).copy()
    m = summ['cnt'].max()
    if m <= 4:
        y_max = 5
    else:
        y_max = m

    # Create countplot
    fig = px.bar(dff
             ,x='Immigration Assignment'
             ,text='Full Name'
             ,labels={
                     "Full Name": "Name",
                     "Age at Deportation": "Age",
                     "Immigration Assignment": "Immigration Assignment",
                     "Immigration Status": "Immigration Status",
                     "Criminal Record": "Criminal History",
                     "Reference":'Sources'
                 }
             ,color_discrete_sequence=px.colors.qualitative.Prism
             ,category_orders={"Immigration Assignment": ["Withholding of Removal", "Temporary Protected Status", "Deportation", "Unknown"]}
            )
    customdata = np.stack((dff['Full Name'], dff['Age at Deportation'], dff['Immigration Status'], dff['Criminal Record'], dff['Reference']), axis=-1)

    fig.update_traces(
        customdata=customdata,
        hovertemplate="<b>%{customdata[0]}</b><br>Age: %{customdata[1]}<br>Assignment: %{x}<br>Status: %{customdata[2]}<br>Criminal History: %{customdata[3]}<br>Sources: %{customdata[4]}<extra></extra>"
    )
    fig.update_layout(yaxis_range=[0, y_max])
    #fig.update_layout(
    #    yaxis={
    #        'showticklabels': False,
    #        'showline': False,
    #    },
    #    yaxis_title=None
    #    )
    #fig.update_layout(title='Count of Men Imprisoned in CECOT by Immigration Assignment', showlegend=False)
    
    fig.update_layout(showlegend=False)

    return stat_cntr, age_cntr, rec_cntr, fig

# Define callback for El Salvador map
@app.callback(
    [Output(component_id='loc_output_container', component_property='children'),
     Output(component_id='map_text', component_property='children'),
     Output(component_id='elsl_map', component_property='figure')],
    [Input(component_id='slct_loc', component_property='value')]
)
def get_map(loc_slctd):

    container = "Selected location: {}".format(loc_slctd)

    dff = loc_df.copy()
    if loc_slctd == 'All':
        lat_=map_init['lat']
        lon_=map_init['lon']
        loc_zoom=8
    else:
        lat_ = dff[dff["Location"] == loc_slctd]['Latitude'].values[0]
        lon_ = dff[dff["Location"] == loc_slctd]['Longitude'].values[0]
        loc_zoom=12

    fig = px.scatter_mapbox(dff, lat='Latitude'
        , lon='Longitude'
        ,text='Location'
        ,mapbox_style="open-street-map"
        #,mapbox_style="satellite-streets"
        ,hover_name="Location"
        ,hover_data=["City", "Department"]
    )

    # Update layout to set zoom and center
    fig.update_layout(
        #mapbox_style='satellite-streets'
        mapbox_zoom=loc_zoom
        ,mapbox_center={"lat": lat_, "lon": lon_}
        ,margin=dict(l=20, r=20, t=20, b=20)
    )

    fig.update_traces(marker=dict(size=20,
                                  color=bbs.marker_color,
                                  opacity=0.5),
                  selector=dict(mode='markers+text'))

    dff2 = map_content_df.copy()
    dff2 = dff2[dff2["Location"] == loc_slctd]

    map_text = html.Div(get_accounts(dff2), style={'fontSize':'1em', 'textAlign':'left'})

    return container, map_text, fig

# Set the start date as the deportation date
deportation_string = "2025-03-15 00:00:00"
format_string = "%Y-%m-%d %H:%M:%S"

deportation_time = dt.strptime(deportation_string, format_string)
start_time = deportation_time

# Define callback for time counter
@app.callback(Output('time-counter', 'children'),
              Input('interval-component', 'n_intervals'))
def update_time(n):
    current_time = dt.now()
    elapsed_time = current_time - start_time
    
    days = elapsed_time.days
    hours, remainder = divmod(elapsed_time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    time_str = f"{days} days, {hours} hours, {minutes} minutes, {seconds} seconds"
    #return html.Span(f"Elapsed time: {time_str}")
    #return html.Span(f"{time_str}")
    return html.Span(f"{time_str}")
    
