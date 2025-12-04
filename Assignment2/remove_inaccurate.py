import pandas as pd
import numpy as np

def remove_inaccurate(input_csv: str, cleaned_csv: str) -> dict:
    df = pd.read_csv(input_csv, low_memory=False)
    num_cols = df.select_dtypes(include=['int64', 'float64']).columns

    rows_before = len(df)

    for col in num_cols:
        df[col] = df[col].replace([np.inf, -np.inf], np.nan)
        mean_val = df[col].mean()
        df[col] = df[col].fillna(mean_val)

        mu = df[col].mean()
        sigma = df[col].std()

        df = df[(df[col] >= mu - 5 * sigma) & (df[col] <= mu + 5 * sigma)]

    df.to_csv(cleaned_csv, index=False)

    return {
        "rows_before": rows_before,
        "rows_after": len(df),
        "removed_rows": rows_before - len(df)
    }
