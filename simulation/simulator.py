import random
import time
from datetime import datetime

from database.db import (
    create_database,
    insert_record
)

BIN_HEIGHT = 50

LOCATIONS = {

    "BIN-001":"School Gate",
    "BIN-002":"Library",
    "BIN-003":"Parking",
    "BIN-004":"Cafeteria",
    "BIN-005":"Admin Block",
    "BIN-006":"Sports Ground",
    "BIN-007":"Bus Stop",
    "BIN-008":"Hostel",
    "BIN-009":"Market Area",
    "BIN-010":"Community Center"
}

def get_status(fill):

    if fill < 30:
        return "EMPTY"

    elif fill < 70:
        return "HALF FULL"

    elif fill < 90:
        return "NEARLY FULL"

    return "FULL"

def get_priority(fill):

    if fill >= 90:
        return "URGENT"

    elif fill >= 70:
        return "HIGH"

    elif fill >= 40:
        return "MEDIUM"

    return "LOW"

create_database()

print("\nSmart Waste Simulator Started\n")

while True:

    for bin_id, location in LOCATIONS.items():

        distance = random.randint(1, 50)

        fill = round(
            ((BIN_HEIGHT - distance)
            / BIN_HEIGHT) * 100,
            2
        )

        status = get_status(fill)

        priority = get_priority(fill)

        alert = (
            "YES"
            if fill >= 90
            else "NO"
        )

        data = {

            "timestamp":
            str(datetime.now()),

            "bin_id":
            bin_id,

            "location":
            location,

            "distance":
            distance,

            "fill_percentage":
            fill,

            "status":
            status,

            "priority":
            priority,

            "alert":
            alert
        }

        insert_record(data)

        print(
            f"{bin_id} | "
            f"{location} | "
            f"{fill}% | "
            f"{status} | "
            f"{priority}"
        )

    print("-" * 70)

    time.sleep(5)