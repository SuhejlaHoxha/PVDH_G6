import pandas as pd
import numpy as np
from pandas.api.types import is_numeric_dtype

def run_transformations(input_csv: str, out_csv: str) -> dict:
    df = pd.read_csv(input_csv, low_memory=False)
    num_cols = [c for c in df.columns if is_numeric_dtype(df[c])]

    col_dict = {}

    for c in num_cols:
        col = df[c].astype(float).values
        finite = np.isfinite(col)
        col = np.where(finite, col, np.nan)

        if np.nanmin(col) >= 0 and np.nanmax(col) > 1.0:
            col_dict[f"{c}__log1p"] = np.log1p(np.nan_to_num(col, nan=0.0))
        else:
            mu = np.nanmean(col)
            sigma = np.nanstd(col)
            if sigma == 0:
                sigma = 1.0
            col_dict[f"{c}__z"] = (np.nan_to_num(col, nan=mu) - mu) / sigma

    out = pd.DataFrame(col_dict, index=df.index)
    out.to_csv(out_csv, index=False)

    return {"numeric_features": len(num_cols), "out_csv": out_csv}
