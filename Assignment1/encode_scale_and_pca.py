import os
import inspect
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.feature_selection import VarianceThreshold
from pandas.api.types import is_numeric_dtype

def _top_k_categorize(series, k=20):
    vc = series.value_counts(dropna=True)
    keep = set(vc.head(k).index.tolist())
    def map_val(v):
        if pd.isna(v):
            return "NA"
        return v if v in keep else "OTHER"
    return series.map(map_val)

def _make_ohe():
    """Create OneHotEncoder that works across sklearn versions."""
    params = {"handle_unknown": "ignore"}
    sig = inspect.signature(OneHotEncoder)
    if "sparse_output" in sig.parameters:
        params["sparse_output"] = False
    else:
        params["sparse"] = False
    return OneHotEncoder(**params)

def run_encode_scale_pca(input_csv: str, encoded_csv: str, pca_csv: str,
                         top_k=20, n_components=10) -> dict:
    df = pd.read_csv(input_csv, low_memory=False)


    os.makedirs(os.path.dirname(encoded_csv), exist_ok=True)
    os.makedirs(os.path.dirname(pca_csv), exist_ok=True)


    numeric_cols = [c for c in df.columns if is_numeric_dtype(df[c])]
    cat_cols = [c for c in df.columns if df[c].dtype == "object"]


    for c in cat_cols:
        df[c] = _top_k_categorize(df[c].astype(str), k=top_k)


    ohe = _make_ohe()
    scaler = StandardScaler(with_mean=True, with_std=True)

    pre = ColumnTransformer(
        [("num", scaler, numeric_cols),
         ("cat", ohe, cat_cols)],
        remainder="drop"
    )

    X_pre = pre.fit_transform(df)


    num_names = numeric_cols
    cat_names = pre.transformers_[1][1].get_feature_names_out(cat_cols).tolist()
    pre_names = num_names + cat_names


    var = VarianceThreshold(threshold=1e-4)
    X = var.fit_transform(X_pre)
    support_mask = var.get_support()
    enc_names = [name for name, keep in zip(pre_names, support_mask) if keep]

    enc_df = pd.DataFrame(X, columns=enc_names)
    enc_df.to_csv(encoded_csv, index=False)


    k = min(n_components, enc_df.shape[1]) if enc_df.shape[1] > 0 else 0
    if k > 0:
        pca = PCA(n_components=k, random_state=42)
        comps = pca.fit_transform(enc_df)
        pca_df = pd.DataFrame(comps, columns=[f"PCA_{i+1}" for i in range(k)])
    else:
        pca_df = pd.DataFrame()

    pca_df.to_csv(pca_csv, index=False)

    return {
        "encoded_features": int(enc_df.shape[1]),
        "pca_components": 0 if pca_df.empty else int(pca_df.shape[1]),
        "encoded_csv": encoded_csv,
        "pca_csv": pca_csv
    }
