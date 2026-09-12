import pandas as pd 
from pathlib import Path
import uuid 

# file modification functions 

def remove_duplicates_rows(df):

    return df.drop_duplicates()

def remove_empty_rows_func(df):

    return df.dropna(how="all")

def remove_empty_columns_func(df):

    return df.dropna(axis=1, how="all")