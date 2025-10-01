import numpy as np
import pandas as pd
# Misc funktions

# Method for handling outliers by clipping
def handle_outliers(df, multiplier=1.5):
    df = df.copy()
    for col in df.select_dtypes(include=["number"]):
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - multiplier * IQR
        upper = Q3 + multiplier * IQR

        # Clip values within bounds
        df[col] = np.clip(df[col], lower, upper)         
    return df

# Method for Filling nulls with median or mean depending on value
def fillna_mean_median(df):
    df = df.copy() 
    for col in df:
        null_count = df[col].isna().sum()
        if null_count > 0:
            mean_val = df[col].mean()
            median_val = df[col].median()
            chosen_val = median_val if abs(mean_val - median_val) > 0.1 * mean_val else mean_val
            df[col] = df[col].fillna(chosen_val)
    return df

# function for splitting up columns by target and dtypes
def split_features_target(df, target_column="Trip_Price"):
    df = df.copy()
    
    # target
    df_target = df[target_column]
    
    # features
    df_features = df.drop(columns=[target_column])
    
    # separate dtypes
    df_categorical = df_features.select_dtypes(include=["object", "category"])
    df_boolean = df_features.select_dtypes(include=["bool"])
    df_numeric = df_features.select_dtypes(include=["int64", "float64"])

    # Combine to X
    X = pd.concat([df_numeric, df_boolean, df_categorical], axis=1)

    return X, df_numeric, df_boolean, df_categorical, df_target


