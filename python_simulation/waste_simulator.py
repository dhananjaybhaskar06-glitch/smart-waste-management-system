import pandas as pd
import random
import time
from datetime import datetime
import os

BIN_HEIGHT = 50
BINS = ["BIN-001", "BIN-002", "BIN-003", "BIN-004"]

csv_file = "data/waste_log.csv"

if not os.path.exists(csv_file):
    pd.DataFrame(columns=[
        "Timestamp",
        "Bin_ID",
        "Distance",
        "Fill_Percentage",
        "Status",
        "Alert"
    ]).to_csv(csv_file, index=False)

def get_status(fill):
    if fill < 30:
        return "EMPTY"
    elif fill < 70:
        return "HALF FULL"
    elif fill < 90:
        return "NEARLY FULL"
    return "FULL"

for cycle in range(100):

    for bin_id in BINS:

        distance = random.randint(1, 50)

        fill = round(
            ((BIN_HEIGHT - distance) / BIN_HEIGHT) * 100,
            2
        )

        status = get_status(fill)

        alert = "YES" if fill >= 90 else "NO"

        row = {
            "Timestamp": datetime.now(),
            "Bin_ID": bin_id,
            "Distance": distance,
            "Fill_Percentage": fill,
            "Status": status,
            "Alert": alert
        }

        pd.DataFrame([row]).to_csv(
            csv_file,
            mode="a",
            header=False,
            index=False
        )

        print(
            f"{bin_id} | "
            f"{fill}% | "
            f"{status}"
        )

    time.sleep(2)