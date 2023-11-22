import re
import pandas as pd
import pdb

def restaurant_validation(df, sheet_name):
    pdb.set_trace()
    not_null_df = df.copy()

# Exclude rows where any column (except 'menu' and 'description') has null values
    not_null_df = not_null_df.dropna(subset=not_null_df.columns.difference(['menu', 'description']))
    return(not_null_df, sheet_name)
