"""Example transformation. Replace it with your own story."""

import pandas as pd


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Drop rows without an id, remove duplicate ids, and parse the order date."""
    out = df.dropna(subset=["order_id"]).drop_duplicates(subset=["order_id"]).copy()
    out["order_date"] = pd.to_datetime(out["order_date"])
    return out
