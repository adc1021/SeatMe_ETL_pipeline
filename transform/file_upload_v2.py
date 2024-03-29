from sqlalchemy import create_engine
import pandas as pd
import os
import pdb
import re
from user_validation import is_valid_phone_number
from user_validation import users_validation
from restaurant_validation import restaurant_validation
import configparser

# pulling variables from config file
def read_config(file_path='/Users/antho/Documents/Job Search - 2023/Port-Proj/SeatMe_ETL/configuration.ini'):
    config = configparser.ConfigParser()
    config.read(file_path)
    # removing the second set of quotation marks being added to the return values
    for section in config.sections():
        for key, value in config.items(section):
            config[section][key] = eval(value)
    return config

config = read_config()

pwd = config['credentials']['pwd']
uid = config['credentials']['uid']
server = config['credentials']['server']
db = config['credentials']['db']
port = config['credentials']['port']
director = config['credentials']['director']
to = config['credentials']['to']
# Initialize rows_imported outside the function
rows_imported = 0

def extract():
    try:
        # starting directory
        directory = director
        # iterate over files in the directory
        for filename in os.listdir(directory):
            # get file name without extension

            file_wo_ext = os.path.splitext(filename)[0]
            # only process excel files
            if filename.endswith(".xlsx"):
                f = os.path.join(directory, filename)
                # checking if it's a file

                if os.path.isfile(f):
                    #iterate over all sheets in the file and use the first row for headers
                    xls = pd.read_excel(f, header=0, sheet_name=None, engine='openpyxl')
                    for sheet_name, df in xls.items():
                        # begin filtering for data cleaning
                        if sheet_name != 'restaurants':
                            print(f"Processing file: {filename}, Sheet: {sheet_name}")
                             # Rows with NaN values
                            nan_rows = df[df.isna().any(axis=1)]
                            # Rows without NaN values
                            clean_df = df.dropna()
                            if sheet_name == 'users':
                                clean_df, sheet_name = users_validation(clean_df, sheet_name)
                        else:
                            print(f"Processing file: {filename}, Sheet: {sheet_name}")
                            clean_df, sheet_name = restaurant_validation(df, sheet_name)
                        load(clean_df, sheet_name)

    except Exception as e:
        print("error while extracting data: " + str(e))

# load data to postgres
def load(clean_df, tbl):
    try:
        # Declare rows_imported as global to ensure variable does not reset
        global rows_imported
        # creating connection to database
        engine = create_engine(f'postgresql://{uid}:{pwd}@{server}:{port}/{db}')
        print(f'importing rows {rows_imported} to {rows_imported + len(clean_df)}...')
        # save df to postgres; method='multi' allows for bulk inserts of rows into db
        clean_df.to_sql(f"stg_{tbl}", engine, if_exists='replace', index=False, method='multi')
        rows_imported += len(clean_df)
        print("Data imported successfully")
    except Exception as e:
        import traceback
        print("Data load error: " + str(e))
        traceback.print_exc()

try:
    extract()
except Exception as e:
    print("Error: " + str(e))
