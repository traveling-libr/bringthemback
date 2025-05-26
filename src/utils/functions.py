# Import general libraries
import pandas as pd

# Import dash libraries
import dash
from dash import html, dcc

"""
DEFINE FUNCTIONS
"""
# Create a long form dataset with one record for each source in SourceIDs
def create_sources_lf(df):
    df['SourceIDs'] = df['SourceIDs'].astype('str')

    desc_ids = []
    src_ids = []

    for idx, row in df.iterrows():
        src_arry = row['SourceIDs'].split(',')
        for i in src_arry:
            desc_ids.append(row['ID'])
            src_ids.append(i)

    lf = pd.DataFrame({'ID':desc_ids,
                        'SourceID':src_ids}).copy()
    lf['SourceID'] = lf['SourceID'].astype('Int64')

    return lf

# Create a dictionary of IDs and formatted bibliographic References related to list of IDs
def get_ref_dict(df):
    df_sorted = df.sort_values(['ID', 'Reference']).copy()
    df_sorted['Reference'] = df_sorted['Reference'].astype('str')
    ref_dict = {}
    for idx, row in df_sorted.iterrows():
        if row['ID'] not in ref_dict:
            ref_dict[row['ID']] = "[" + row['Reference'] + "]"
        else:
            ref_dict[row['ID']] = ref_dict[row['ID']] + ", [" + row['Reference'] + "]"
    return ref_dict

def get_ref_dict_lnkd(df):
    ids = df['ID'].unique().tolist()
    ref_dict = {}
    for id in ids:
        id_df = df.loc[df['ID']==id].copy()
        refs = sorted(id_df['Reference'].to_list())
        url_dict = id_df.set_index('Reference')['URL'].to_dict()
        for j in range(0, len(refs)):
            if j == 0:
                ref_list = []
                ref_list.append(html.Span("["))
            else:
                ref_list.append(html.Span(", ["))
            ref_list.append(html.Span(dcc.Link(refs[j], href=url_dict[refs[j]], target="_blank", style={'text-decoration':'none'})))
            ref_list.append(html.Span("]"))
        ref_dict[id] = html.Sup(ref_list)
    
    return ref_dict

# Create list of paragraphs with associated bibliographic references
def get_accounts(df, rtype='list'):
    if rtype=='list':
        accounts_dict = df.set_index('Account')['Reference_lnkd'].to_dict()
        accounts = []
        for k, v in accounts_dict.items():
            r = html.P([k, v])
            accounts.append(r)
    elif rtype=='dict':
        df['combined'] = df[['Title', 'Account', 'Reference_lnkd']].values.tolist()
        accounts_dict = df.set_index('SectionID')['combined'].to_dict()
        accounts = {}
        for k, v in accounts_dict.items():
            if v[0] in accounts:
                accounts[v[0]].append(html.P([v[1], v[2]]))
            else:
                accounts[v[0]] = []
                accounts[v[0]].append(html.P([v[1], v[2]]))
    return accounts

def try_parse_int(x):
  try:
    return int(x)
  except:
    return None