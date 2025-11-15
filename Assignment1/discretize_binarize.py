import os
import warnings
import inspect
import pandas as pd
import numpy as np
from sklearn.preprocessing import KBinsDiscretizer
from pandas.api.types import is_numeric_dtype


def _make_kbins(n_bins=4):
    kwargs = {"n_bins": n_bins, "encode": "ordinal", "strategy": "quantile"}
    sig = inspect.signature(KBinsDiscretizer)
    if "quantile_method" in sig.parameters:
        kwargs["quantile_method"] = "averaged_inverted_cdf"
    return KBinsDiscretizer(**kwargs)


def run_discretize_binarize(input_csv: str, disc_csv: str, bin_csv: str, n_bins=4) -> dict:
    warnings.filterwarnings("ignore", message="Bins whose width are too small")
    df = pd.read_csv(input_csv, low_memory=False)
    os.makedirs(os.path.dirname(disc_csv), exist_ok=True)
    os.makedirs(os.path.dirname(bin_csv), exist_ok=True)

    num_cols = [c for c in df.columns if is_numeric_dtype(df[c])]

    disc_dict = {}
    bin_dict = {}

    if num_cols:
        num = df[num_cols].copy()
        num = num.fillna(num.median(numeric_only=True))

        for c in num.columns:
            s = num[c].astype(float)
            uniq_count = s.dropna().nunique()

            if uniq_count <= 1:
                disc_dict[f"{c}__qbin"] = np.zeros(len(s))
                continue

            bins_here = min(n_bins, uniq_count)

            try:
                kb = _make_kbins(n_bins=bins_here)
                result = kb.fit_transform(s.to_frame()).ravel()

                if len(np.unique(result)) < 2:
                    disc_dict[f"{c}__qbin"] = pd.qcut(
                        s.rank(method="first"),
                        q=min(uniq_count, n_bins),
                        labels=False,
                        duplicates="drop"
                    )
                else:
                    disc_dict[f"{c}__qbin"] = result

            except Exception:
                disc_dict[f"{c}__qbin"] = pd.qcut(
                    s.rank(method="first"),
                    q=min(uniq_count, n_bins),
                    labels=False,
                    duplicates="drop"
                )

        med = num.median(numeric_only=True)
        for c in num.columns:
            m = med.get(c, 0.0)
            bin_dict[f"{c}__bin"] = (num[c] > m).astype(int)

    disc_df = pd.DataFrame(disc_dict)
    bin_df = pd.DataFrame(bin_dict)

    disc_df.to_csv(disc_csv, index=False)
    bin_df.to_csv(bin_csv, index=False)

    return {
        "numeric_features": len(num_cols),
        "disc_csv": disc_csv,
        "bin_csv": bin_csv
    }
