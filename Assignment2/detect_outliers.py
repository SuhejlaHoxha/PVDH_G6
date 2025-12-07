import pandas as pd

def detect_outliers_and_save_dataset(input_csv: str, clean_output_csv: str, outliers_output_csv: str) -> dict:
    df_original = pd.read_csv(input_csv, low_memory=False)
    df = df_original.copy()
    original_len = len(df)

    outlier_reasons = pd.Series("", index=df_original.index) 

    num_cols = df.select_dtypes(include=['int64', 'float64']).columns
    numeric_mask = pd.Series(False, index=df.index)

    for col in num_cols:
        Q1 = df_original[col].quantile(0.25)
        Q3 = df_original[col].quantile(0.75)
        IQR = Q3 - Q1
        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        mask_col = (df_original[col] < lower) | (df_original[col] > upper)
        outlier_reasons[mask_col] += f"IQR outlier in {col}; "
        numeric_mask |= mask_col

    str_cols = df.select_dtypes(include=['object', 'string']).columns
    categorical_mask = pd.Series(False, index=df_original.index)

    for col in str_cols:
        nunique = df_original[col].nunique()
        if nunique > 0.9 * len(df_original):
            continue

        value_counts = df_original[col].value_counts()
        threshold = 0.01 * len(df_original)
        rare_values = value_counts[value_counts < threshold].index

        mask_col = df_original[col].isin(rare_values)
        outlier_reasons[mask_col] += f"Rare value in {col}; "
        categorical_mask |= mask_col

    total_mask = numeric_mask | categorical_mask

    df_clean = df_original[~total_mask].copy()
    outliers_df = df_original[total_mask].copy()
    outliers_df["outlier_reason"] = outlier_reasons[total_mask]

    df_clean.to_csv(clean_output_csv, index=False)
    outliers_df.to_csv(outliers_output_csv, index=False)

    return {
        "original_rows": original_len,
        "cleaned_rows": len(df_clean),
        "outlier_rows": len(outliers_df),
        "removed_rows": original_len - len(df_clean),
        "cleaned_saved_to": clean_output_csv,
        "outliers_saved_to": outliers_output_csv
    }
