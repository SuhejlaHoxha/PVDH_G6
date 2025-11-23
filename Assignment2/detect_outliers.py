import pandas as pd
import numpy as np

def detect_outliers(input_csv: str) -> dict:
    df = pd.read_csv(input_csv, low_memory=False)

    num_cols = df.select_dtypes(include=['int64', 'float64']).columns
    outlier_counts = {}

    for col in num_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1

        lower = Q1 - 1.5 * IQR
        upper = Q3 + 1.5 * IQR

        outliers = df[(df[col] < lower) | (df[col] > upper)]
        outlier_counts[col] = len(outliers)

    return {
        "total_numeric_columns": len(num_cols),
        "outliers_per_column": outlier_counts
    }
