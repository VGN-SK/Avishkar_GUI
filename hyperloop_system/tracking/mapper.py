from backend.pod_service import get_pod_by_name
from backend.telemetry_service import get_latest_telemetry
from tracking.default_tracks import get_track

from backend.telemetry_service import get_all_latest_snapshots
from backend.pod_service import get_all_pods


# GET POD'S CURRENT MAP POSITION

def get_pod_coordinates(pod_name: str): #Returns current latitude and longitude for pod.

    # Get pod metadata
    pod = get_pod_by_name(pod_name)
    if not pod:
        return None

    # Get latest telemetry
    telemetry = get_latest_telemetry(pod_name)
    if not telemetry:
        return None

    position_m = float(telemetry["position_m"])

    # Get track model
    track = get_track(pod["track_id"])

    # Convert position to lat/lon
    lat, lon = track.get_coordinates(position_m)

    return {
        "pod_name": pod_name,
        "lat": lat,
        "lon": lon,
        "velocity": float(telemetry["velocity"]),
        "status": pod["status"]
    }



# GET ALL PODS MAP SNAPSHOT

def get_all_pod_coordinates(): #Returns map-ready snapshot for all pods.

    snapshots = get_all_latest_snapshots()
    pods = get_all_pods()

    result = []

    for pod in pods:

        name = pod["name"]

        if name not in snapshots:
            continue

        position_m = float(snapshots[name]["position_m"])

        track = get_track(pod["track_id"])
        lat, lon = track.get_coordinates(position_m)

        result.append({
            "pod_name": name,
            "lat": lat,
            "lon": lon,
            "velocity": float(snapshots[name]["velocity"]),
            "status": pod["status"]
        })

    return result

