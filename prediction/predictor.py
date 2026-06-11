import pandas as pd
import sqlite3
import numpy as np
from sklearn.linear_model import LinearRegression

DB_PATH = "data/waste_management.db"

def predict_fill_levels():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT *
    FROM waste_data
    """

    df = pd.read_sql(query, conn)

    conn.close()

    if len(df) < 10:
        return None

    results = {}

    for bin_id in df["bin_id"].unique():

        bin_data = df[
            df["bin_id"] == bin_id
        ]

        bin_data = bin_data.tail(20)

        if len(bin_data) < 5:
            continue

        X = np.arange(
            len(bin_data)
        ).reshape(-1,1)

        y = bin_data[
            "fill_percentage"
        ]

        model = LinearRegression()

        model.fit(X,y)

        future_fill = model.predict(
            [[len(bin_data)+5]]
        )[0]

        future_fill = max(
            0,
            min(100,future_fill)
        )

        results[bin_id] = round(
            future_fill,
            2
        )

    return results