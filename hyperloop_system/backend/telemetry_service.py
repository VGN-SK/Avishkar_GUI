import csv
from pathlib import Path
from collections import deque


LOG_FILE = Path("data/telemetry_log.csv")
SNAPSHOT_FILE = Path("data/latest_snapshot.csv")


# GET LATEST TELEMETRY FOR POD - FROM THE LOG SNAPSHOT CSV FILE

def get_latest_telemetry(pod_name: str):
    """
    O(1) read from snapshot file.
    """
    if not SNAPSHOT_FILE.exists():
        return None

    with open(SNAPSHOT_FILE, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if row["pod_name"] == pod_name:
                return row

    return None


# GET RECENT TELEMETRY HISTORY - SOME LATEST ENTRIES - CAN BE USED FOR CANCELLING NOISE IN VELOCITY OR OTHER VALUES USING ROLLING MEAN

def get_recent_telemetry(pod_name: str, limit: int = 50):
    """
    Reads from historical log file.
    """
    if not LOG_FILE.exists():
        return []

    buffer = deque(maxlen=limit)

    with open(LOG_FILE, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if row["pod_name"] == pod_name:
                buffer.append(row)

    return list(buffer)


# GET ALL POD LATEST TELEMETRY DETALS
def get_all_latest_snapshots():
    """
    Returns dictionary of latest packets per pod.
    """
    if not SNAPSHOT_FILE.exists():
        return {}

    snapshots = {}

    with open(SNAPSHOT_FILE, "r") as f:
        reader = csv.DictReader(f)

        for row in reader:
            snapshots[row["pod_name"]] = row

    return snapshots

