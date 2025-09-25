import numpy as np
import pandas as pd
# Misc funktions

# Method for handling outliers by removing or clipping
def handle_outliers(df, cols, multiplier=1.5):
    df_removed = df.copy()
    df_clipped = df.copy()

    # Create a combined mask for all numeric columns
    mask = pd.Series(True, index=df.index)

    for col in cols:
        if df[col].dtype != 'object':
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower = Q1 - multiplier * IQR
            upper = Q3 + multiplier * IQR

            # Update mask for removal
            mask &= (df[col] >= lower) & (df[col] <= upper)

            # Clip values within bounds
            df_clipped[col] = np.clip(df[col], lower, upper)

    # Apply final mask to remove rows with any numeric outliers
    df_removed = df[mask]

    return df_removed, df_clipped

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
    df_target = df[[target_column]]

    categorical_columns = df.select_dtypes(include=["object"]).columns
    df_categorical = df[categorical_columns]

    numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns.drop(target_column)
    df_numeric = df[numeric_columns]

    return df_numeric, df_categorical, df_target


