# Import general libraries
import pandas as pd
import numpy as np

# Import local libraries
from .functions import *
from .data import *

# Import general libraries
import pandas as pd

"""
CREATE AND INITIALIZE VARIABLES FOR ACCOUNTS
"""
section_dict = {'immigration_account':1,
                'family':2,
                'criminal_history':3,
                'map':1
                }

"""
CREATE NEW VARIABLES IN TEXT AND ACCOUNT DATASETS
"""
text_df_sorted = text_df.sort_values(['Section', 'Order']).copy()
text_df_sorted['Title'] = [x.replace('_', ' ').title() for x in text_df_sorted['Section']]
text_df_sorted['SectionID'] = [i + "_" + str(j) for (i, j) in zip(text_df_sorted['Section'], text_df_sorted['Order'])]

accounts_df['Order'] = [section_dict[x] for x in accounts_df['Section']]
acct_df_sorted = accounts_df.sort_values(['Section', 'Order', 'Second Order']).copy()
acct_df_sorted['Order'] = [section_dict[x] for x in acct_df_sorted['Section']]
acct_df_sorted['Title'] = [x.replace('_', ' ').title() for x in acct_df_sorted['Section']]
acct_df_sorted['SectionID'] = [i + "_" + str(j) + "_" + str(k) for (i, j, k) in zip(acct_df_sorted['Section'], acct_df_sorted['Order'], acct_df_sorted['Second Order'])]

"""
REFERENCE DATA - CREATE BIBLIOGRAPHY AND REFERENCES
"""
# CREATE REFERENCE NUMBERS

src_df_sorted = src_df.sort_values('Bibliographic Reference').copy()
src_df_sorted['Reference'] = src_df_sorted.groupby('Bibliographic Reference').ngroup() + 1

references = src_df_sorted.copy()
#references.to_csv('data_references/references.csv', index=False)

men_src_lf = create_sources_lf(all_men_df.loc[all_men_df['SourceIDs'].notna()].copy())
#men_src_lf.to_csv('data_references/men_references.csv', index=False)

accounts_src_lf = create_sources_lf(acct_df_sorted.copy())
#accounts_src_lf.to_csv('data_references/accounts_references.csv', index=False)

text_src_lf = create_sources_lf(text_df_sorted.loc[text_df_sorted['SourceIDs'].notna()].copy())
#text_src_lf.to_csv('data_references/text_references.csv', index=False)

# MATCH REFERENCES TO BIBLIOGRAPHIC REFERENCES AND ADD TO DATAFRAMES

men_ref = pd.merge(men_src_lf, references, on='SourceID', how='left').copy()
men_ref_dict = get_ref_dict(men_ref)
all_men_df['Reference'] = [np.nan if str(x)=='nan' else men_ref_dict[int(x)] for x in all_men_df['ID']]
men_ref_dict_lnkd = get_ref_dict_lnkd(men_ref)
all_men_df['Reference_lnkd'] = [np.nan if str(x)=='nan' else men_ref_dict_lnkd[int(x)] for x in all_men_df['ID']]

text_ref = pd.merge(text_src_lf, references, on='SourceID', how='left').copy()
text_ref_dict = get_ref_dict(text_ref)
text_df_sorted['Reference'] = [np.nan if (try_parse_int(x) == None) else np.nan if int(x) not in text_ref_dict else text_ref_dict[int(x)] for x in text_df_sorted['ID']]
text_ref_dict_lnkd = get_ref_dict_lnkd(text_ref)
text_df_sorted['Reference_lnkd'] = [np.nan if (try_parse_int(x) == None) else np.nan if int(x) not in text_ref_dict else text_ref_dict_lnkd[int(x)] for x in text_df_sorted['ID']]

accounts_ref = pd.merge(accounts_src_lf, references, on='SourceID', how='left').copy()
accounts_ref_dict = get_ref_dict(accounts_ref)
acct_df_sorted['Reference'] = [accounts_ref_dict[int(x)] for x in acct_df_sorted['ID']]
accounts_ref_dict_lnkd = get_ref_dict_lnkd(accounts_ref)
acct_df_sorted['Reference_lnkd'] = [accounts_ref_dict_lnkd[int(x)] for x in acct_df_sorted['ID']]

"""
SPLIT ACCOUNTS INTO MEN AND LOCATIONS
"""
men_acct_df = acct_df_sorted.loc[acct_df_sorted['Entity']=='M'].copy()
loc_acct_df = acct_df_sorted.loc[acct_df_sorted['Entity']=='L'].copy()

"""
INIALIZE VARIABLES FOR 'THE MEN'
"""
mid_init = 1

"""
CREATE VARIABLES AND GROUPS FOR 'HOME', 'THE MEN', AND 'SUMMARY'
"""
all_men_df['Age Group'] = ['0-4' if x <= 4 else '5-14' if x <= 14 else '15-24' if x <= 24 else '25-34' if x <= 34 else '35-44' if x <= 44 else '45-54' if x <= 54 else '55-64' if x <= 64 else 'Unknown' for x in all_men_df['Age at Deportation'] ]
all_men_df['Full Name'] = [i + ' ' + j for (i, j) in zip(all_men_df['First Name'], all_men_df['Last Name'])]
all_men_df['Reverse Name'] = all_men_df['Last Name'] + ", " + all_men_df['First Name']

"""
CREATE DICTIONARY OF ACCOUNTS FOR 'ABOUT'
"""
app_text = get_accounts(text_df_sorted, rtype='dict')

"""
CREATE DATAFRAME FOR NAMES ON 'HOME'
"""
names_df = all_men_df.loc[:,['First Name', 'Last Name', 'Reverse Name']].sort_values(['Last Name', 'First Name']).copy()
names_df['Rank'] = names_df.groupby(['Reverse Name']).ngroup() + 1
names_df['Group'] = [x % 2 for x in names_df['Rank']]

""" 
CREATE DATAFRAME FOR 'SUMMARY'
"""
men_df = all_men_df.loc[all_men_df['SourceIDs'].notna()].sort_values(['Last Name','First Name']).copy()

bar_init = {}
bar_init['stat'] = 'All'
bar_init['age'] = 'All'
bar_init['rec'] = 'All'

stat_init = 'All'
stat_dict = {'All':'All'}
for e in sorted(men_df['Immigration Status'].unique().tolist()):
    stat_dict[e] = e

age_init = 'All'
age_dict = {'All':'All'}
for e in sorted(men_df['Age Group'].unique().tolist()):
    age_dict[e] = e

rec_init = 'All'
rec_dict = {'All':'All'}
for e in sorted(men_df['Criminal Record'].unique().tolist()):
    rec_dict[e] = e

bar_dict = {}
bar_dict['stat'] = stat_dict
bar_dict['age'] = age_dict
bar_dict['rec'] = rec_dict

"""
CREATE DATASETS AND INITIALIZE VARIABLES FOR 'THE PRISONS'
"""
loc_list = ['All'] + sorted(loc_df['Location'].unique().tolist())
map_init = {}
map_init['loc'] = 'All'
map_init['lat'] = 13.6929
map_init['lon'] = -89.2182

# Merge loc_acct_df with loc_df for content and geographic data for map
map_content_init = pd.merge(loc_acct_df, loc_df, left_on='EID', right_on='ID', how='left').copy()

# Select data only if prison is in loc_df
# Sort by LOCATION ad ORDER to display paragraphs in chosen order for each location
prisons = loc_df.Location.unique().tolist()
map_content_df = map_content_init.loc[map_content_init['Location'].isin(prisons)].sort_values(['Location','Order']).copy()
