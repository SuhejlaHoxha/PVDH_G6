import pandas as pd


def data_quality_check(csv_path: str):
    df = pd.read_csv(csv_path)

    missing = df.isnull().sum()
    print("Missing values per column:\n", missing, "\n")

    dup_count = df.duplicated().sum()
    print(f"Duplicate rows: {dup_count}\n")

    empty_strings = {}
    for col in df.columns:
        if df[col].dtype == object:
            empty_strings[col] = df[col].astype(str).str.strip().eq("").sum()
        else:
            empty_strings[col] = 0
    print("Empty string values per column:\n", pd.Series(empty_strings), "\n")

    for col in df.columns:
        if "time" in col.lower():
            try:
                pd.to_datetime(df[col])
            except:
                print(f"[WARNING] Column '{col}' has invalid datetime values")
