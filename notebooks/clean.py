import pandas as pd
import numpy as np

def clean_missing_values(data_df: pd.DataFrame)->pd.DataFrame:
    """
    Returns input DataFrame with columns having more than 40%
    of its values being missing values dropped
    """
    threshold = 0.6
    data_df = data_df.dropna(axis=1, thresh=int((1-threshold)*data_df.shape[0]))
    
    return data_df

def format_values(data_df: pd.DataFrame)->pd.DataFrame:
    """
    Returns the input dataframe with a consistent
    format applied to all column values 
    """
    global int_cols, categorical_cols, date_cols, float_cols, cols_to_clean
    int_cols = ["Number of Buildings"]
    categorical_cols = data_df.loc[:,"Property Id":"Primary Property Type - Self Selected"].columns.to_list() + ["Unique ID"]
    date_cols = ["Year Ending","Year Built"]
    float_cols = data_df.columns.difference(int_cols+date_cols+categorical_cols).to_list()

    cols_to_clean = ["Property GFA - Self-Reported (m²)",
    "Site Energy Use (GJ)",                                                   
    "Weather Normalized Site Energy Use (GJ)",
    "Source Energy Use (GJ)",                                                 
    "Weather Normalized Source Energy Use (GJ)",
    "Total GHG Emissions (Metric Tons CO2e)",
    "Direct GHG Emissions (Metric Tons CO2e)",  
    "Electricity Use - Grid Purchase (kWh)",                                  
    "Natural Gas Use (GJ)"
    ]
    
    # Removes commas from numbers 
    # that use a comma as the thousands separator
    reg = "(((\d{1,3}),)*(\d{1,3})(\.\d+)?)"
    for col in cols_to_clean:
        a = data_df[col][data_df[col].str.contains(",", na=False)].str.extract(reg)
        b = a.apply(lambda row: row[2:].str.cat(), axis=1)
        data_df.loc[b.index, col] = b
    
    # Applies consistent format "A1A 1A1" to all
    # postal codes
    frmt = lambda val : val.strip().upper().replace(" ", "")[:3] + " " + val.strip().upper().replace(" ", "")[3:]
    r = "([A-Z][0-9][A-Z] [0-9][A-Z][0-9])"
    ind = np.invert(data_df["Postal Code"].str.contains(r,regex=True))
    data_df.loc[ind,"Postal Code"] = data_df["Postal Code"][ind].apply(frmt)
    
    # Applies the following format to all adresses
    # - Puts words that come before suffix in title case
    # - Puts suffix in uppercase
    frmt = lambda val : " ".join([str(val.values[0]).strip().title(), str(val.values[1]).strip().upper()])
    r = "(.+) (\w+ \w+)$"
    extrcts = data_df["Address 1"].str.extract(r)
    data_df.loc[extrcts.index,"Address 1"] = extrcts.apply(frmt, axis=1)
        
    return data_df

def impute_values(data_df: pd.DataFrame)->None:
    """
    Imputes column missing values
    inplace with either column median(for numeric)
    or column mode(for categorical)
    """
    fill = {}

    data_df.loc[:,cols_to_clean] = data_df.loc[:,cols_to_clean].astype("float64")

    for colname in int_cols + float_cols:
        fill[colname] = data_df.loc[:,colname].median()
        
    for colname in categorical_cols:
        fill[colname] = data_df.loc[:,colname].mode()[0]
        
    data_df.fillna(fill, inplace=True)
    
def clean_outliers(data_df: pd.DataFrame)->None:
    """
    Replace outlier values with column
    median values inplace
    """
    Q1 = data_df["Total GHG Emissions (Metric Tons CO2e)"].quantile(0.25)
    Q3 = data_df["Total GHG Emissions (Metric Tons CO2e)"].quantile(0.75)
    IQR = Q3 - Q1

    col = "Total GHG Emissions (Metric Tons CO2e)"
    outliers = data_df[col][(data_df[col] < Q1 - (1.5*IQR))|(data_df[col] > Q3 + (1.5*IQR))]
    outlier_p_types = data_df.loc[outliers.index,"Primary Property Type - Self Selected"]

    for i in outliers.index:
        data_df.loc[i,col] = data_df[data_df["Primary Property Type - Self Selected"]==outlier_p_types[i]][col].median()

