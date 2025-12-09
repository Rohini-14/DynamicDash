import pandas as pd
import numpy as np

def read_any(file):
    name = getattr(file, "name", "uploaded")
    if str(name).lower().endswith((".xlsx", ".xls")):
        df = pd.read_excel(file)
    else:
        df = pd.read_csv(file)
    return df

def auto_etl(df):
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]
    df = df.dropna(axis=1, how="all")
    df = df.drop_duplicates()
    for c in df.columns:
        if df[c].dtype == "object":
            try:
                parsed = pd.to_datetime(df[c], errors="raise")
                if parsed.notna().sum() >= 0.8 * len(parsed):
                    df[c] = parsed
            except Exception:
                pass
    for c in df.columns:
        if pd.api.types.is_numeric_dtype(df[c]):
            df[c] = df[c].fillna(df[c].median())
        else:
            if df[c].isna().any():
                mode = df[c].mode(dropna=True)
                df[c] = df[c].fillna(mode.iloc[0] if not mode.empty else "Unknown")
    return df
