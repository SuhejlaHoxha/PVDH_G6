import pandas as pd

def clean_dataset(input_csv: str, output_csv: str):
    df = pd.read_csv(input_csv)

    # A) Heq rreshtat krejtësisht bosh
    df.dropna(how="all", inplace=True)

    # Heq kolonat krejtësisht bosh
    df.dropna(axis=1, how="all", inplace=True)

    # B) Fix datat tek kolonat që përmbajnë "timestamp"
    for col in df.columns:
        if "timestamp" in col.lower():
            df[col] = pd.to_datetime(df[col], errors="coerce")  

    # C) Trim & lowercase + trajtim i vlerave bosh tek kolonat string
    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].astype(str).str.strip().str.lower()
        df[col] = df[col].replace({"nan": "unknown", "none": "unknown", "": "unknown"})

    # D) Trajtim i vlerave bosh tek kolonat boolean
    for col in df.select_dtypes(include=["bool"]).columns:
        df[col] = df[col].fillna(False)  # ose True sipas nevojës

    # E) Trajtim i vlerave bosh tek kolonat numerike
    for col in df.select_dtypes(include=["int64", "float64"]).columns:
        df[col] = df[col].fillna(0)  

    df.to_csv(output_csv, index=False)
    print(f"Dataset cleaned and saved to: {output_csv}")
