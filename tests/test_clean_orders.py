import pandas as pd

from src.clean_orders import clean_orders


def test_drops_missing_ids_and_duplicates():
    df = pd.DataFrame(
        {
            "order_id": [1, 1, None, 2],
            "order_date": ["2026-01-01", "2026-01-01", "2026-01-02", "2026-01-03"],
        }
    )
    result = clean_orders(df)
    assert list(result["order_id"]) == [1, 2]


def test_parses_dates():
    df = pd.DataFrame({"order_id": [1], "order_date": ["2026-01-01"]})
    assert str(clean_orders(df)["order_date"].dtype).startswith("datetime64")
