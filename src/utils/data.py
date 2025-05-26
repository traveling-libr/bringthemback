# Import general libraries
import pandas as pd

"""
READ CSV - CONTENT DATA
"""
data_repo = "https://raw.githubusercontent.com/traveling-libr/data/refs/heads/main/bringthemback/"

src_df = pd.read_csv(data_repo + 'sources.csv')
loc_df = pd.read_csv(data_repo + 'locations.csv')
all_men_df = pd.read_csv(data_repo + 'the_men.csv')
text_df = pd.read_csv(data_repo + 'app_text.csv')
accounts_df = pd.read_csv(data_repo + 'accounts.csv')

