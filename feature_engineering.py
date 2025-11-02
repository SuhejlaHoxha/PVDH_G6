
import pandas as pd
import numpy as np
import re
import ipaddress
from pandas.api.types import is_datetime64_any_dtype

def _extract_action(s):
    if not isinstance(s, str):
        return np.nan
    parts = s.split(".")
    return parts[-1] if parts else s

def _service_short(s):
    if not isinstance(s, str):
        return np.nan
    return s.split(".")[0]

def _resource_type_short(s):
    if not isinstance(s, str):
        return np.nan
    return s.split(".")[-1]

def _ip_is_private(x):
    try:
        ip = ipaddress.ip_address(str(x))
        return int(ip.is_private)
    except Exception:
        return np.nan

def _ip_first_octet(x):
    try:
        return int(str(x).split(".")[0])
    except Exception:
        return np.nan

def _datetime_parts(df, col):
    out = pd.DataFrame(index=df.index)
    out[f"{col}__year"]   = df[col].dt.year
    out[f"{col}__month"]  = df[col].dt.month
    out[f"{col}__day"]    = df[col].dt.day
    out[f"{col}__hour"]   = df[col].dt.hour
    out[f"{col}__dow"]    = df[col].dt.dayofweek
    out[f"{col}__is_weekend"] = (out[f"{col}__dow"].isin([5,6])).astype(int)
    return out

def run_feature_engineering(input_csv: str, output_csv: str) -> dict:
    df = pd.read_csv(input_csv, low_memory=False)


    datetime_like_cols = [c for c in df.columns if re.search(r"(time|date)", c, re.IGNORECASE)]
    for c in datetime_like_cols:
        try:
            df[c] = pd.to_datetime(df[c], errors="coerce", utc=True)
        except Exception:
            pass


    df["method_action"] = df.get("protoPayload.methodName", pd.Series([np.nan]*len(df))).apply(_extract_action)
    df["service_short"] = df.get("protoPayload.serviceName", pd.Series([np.nan]*len(df))).apply(_service_short)
    df["resource_type_short"] = df.get("resource.type", pd.Series([np.nan]*len(df))).apply(_resource_type_short)

    if "protoPayload.requestMetadata.callerIp" in df.columns:
        ip_col = "protoPayload.requestMetadata.callerIp"
        df["callerIp_is_private"] = df[ip_col].apply(_ip_is_private)
        df["callerIp_first_octet"] = df[ip_col].apply(_ip_first_octet)


    dt_frames = []
    for c in datetime_like_cols:
        if c in df and is_datetime64_any_dtype(df[c]):
            dt_frames.append(_datetime_parts(df, c))
    if dt_frames:
        df = pd.concat([df] + dt_frames, axis=1)

    df.to_csv(output_csv, index=False)

    return {
        "rows": len(df),
        "cols": len(df.columns),
        "datetime_cols": datetime_like_cols,
        "output_csv": output_csv
    }
