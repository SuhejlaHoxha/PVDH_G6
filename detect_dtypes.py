import pandas as pd
import warnings

warnings.filterwarnings(
    "ignore",
    message="Could not infer format",
    category=UserWarning
)

def detect_dtypes(csv_path: str):
    df = pd.read_csv(csv_path)

    for col in df.columns:
        try:
            df[col] = pd.to_datetime(df[col])
        except Exception:
            pass

    detected = {}
    for col, dtype in df.dtypes.items():
        if pd.api.types.is_integer_dtype(dtype):
            detected[col] = "int"
        elif pd.api.types.is_float_dtype(dtype):
            detected[col] = "float"
        elif pd.api.types.is_bool_dtype(dtype):
            detected[col] = "bool"
        elif pd.api.types.is_datetime64_any_dtype(dtype):
            detected[col] = "datetime"
        else:
            detected[col] = "string"

    return detected
