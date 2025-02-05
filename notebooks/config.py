import clean

def main():
    raw_data_path = "../data/raw/Building_Energy_Benchmarking.csv"
    raw_df = clean.pd.read_csv(raw_data_path)
    clean_df = clean.clean_missing_values(raw_df)
    clean_df = clean.format_values(clean_df)
    clean.impute_values(clean_df)
    clean.clean_outliers(clean_df)

    return raw_df, clean_df

raw_df, clean_df = main()