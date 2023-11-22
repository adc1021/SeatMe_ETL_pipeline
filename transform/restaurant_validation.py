import re
import pandas as pd
import pdb
from user_validation import is_valid_phone_number, validate_column


def restaurant_validation(df, sheet_name):
    not_null_df = df.copy()

    # Exclude rows where any column (except 'menu' and 'description') has null values
    not_null_df = not_null_df.dropna(subset=not_null_df.columns.difference(['menu', 'description']))
    validate_column(not_null_df, 'phone_number', is_valid_phone_number, 'is_valid_phone', sheet_name)
    clean_df = not_null_df.loc[(not_null_df['is_valid_phone'] != False)]

    return(clean_df, sheet_name)
