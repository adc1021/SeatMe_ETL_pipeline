import re
import pandas as pd

#function that directs each row to the distinct function designed to filter it's values
def validate_column(clean_df, column_name, validation_function, result_column_name, tbl):
    if column_name in clean_df.columns:
        clean_df[result_column_name] = clean_df[column_name].apply(validation_function)
        invalid_entries = clean_df.loc[clean_df[result_column_name] == False]

        if not invalid_entries.empty:
            print(f"Invalid {column_name} entries found in {tbl} sheet:")
            print(invalid_entries[[column_name]])
    return

# validates users information prior to loading into db
def users_validation(clean_df, tbl):
    validate_column(clean_df, 'phone_number', is_valid_phone_number, 'is_valid_phone', tbl)
    validate_column(clean_df, 'email', is_valid_email, 'is_valid_email', tbl)

    clean_df = clean_df.loc[(clean_df['is_valid_phone'] != False) & (clean_df['is_valid_email'] != False)]

    return clean_df, tbl

# checks to ensure valid phone number formatting
def is_valid_phone_number(phone_number):
    if pd.isna(phone_number) or not isinstance(phone_number, str):
        return False

    pattern = re.compile(r'^\D*(\d{3})\D*(\d{3})\D*(\d{4})\D*$')
    return bool(pattern.match(phone_number))

# checks to ensure valid email formatting
def is_valid_email(email):
    if pd.isna(email) or not isinstance(email, str):
        return False

    pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return bool(pattern.match(email))
