
#-----------------date_process----------------------
def date_process(x):
    """
    Function that converts a float value into a pandas datestamp.
    This function can takes both date and datetime formats.
    x = accepts float with length 14 or 8, no special characters
    returns x as timestamp
        if x is null, returns string 'error', 
        if x is of a length other than 14 or 4, returns string 'error'.
    """
    if x > 0:
        x = str(round(x))
        if len(x) == 14: 
            return pd.to_datetime(x, format="%Y%m%d%H%M%S")
            
        elif len(x) == 8:
            return pd.to_datetime(x, format="%Y%m%d") 
                        
        else:
            return 'error'
    else:
        return 'error'
#----------------------------------------------------
#-----------------drop_null_30----------------------
def drop_null_30(df):
    """
    drops all columns from input df with missing data of over 30%
    """
    percent_missing = round(df.isnull().sum() * 100 / len(df))
    missing_values = pd.DataFrame({'column_name': df.columns, 'percent_missing': percent_missing})
    
    cols_30 = missing_values[missing_values['percent_missing'] > 30].index
    df.drop(cols_30, inplace=True, axis = 1)
    return f'The following columns have been dropped: {cols_30}'
#----------------------------------------------------