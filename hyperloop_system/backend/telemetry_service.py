import csv
from pathlib import Path
from collections import deque

from backend.pod_service import get_pod_by_name
from tracking.default_tracks import get_track

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
    
def move_pod_forward(pod_name: str, distance_m: float):

    rows = []
    updated = False

    with open(SNAPSHOT_FILE, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:

            if row["pod_name"] == pod_name:

                pod_meta = get_pod_by_name(pod_name)
                track = get_track(pod_meta["track_id"])

                current_position = float(row["position_m"])
                new_position = current_position + distance_m

                if new_position > track.total_length:
                    new_position = track.total_length

                row["position_m"] = str(new_position)
                updated = True

            rows.append(row)

    if updated:
        with open(SNAPSHOT_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

