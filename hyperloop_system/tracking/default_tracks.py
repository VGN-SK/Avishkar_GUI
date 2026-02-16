from tracking.waypoint import Waypoint
from tracking.track_model import TrackModel


def get_track(track_id: str):   # TO GET TRACK CORRSPONDING TO ID.. CURRENTLY ONLY HARDCODED.. WILL MAKE IT DYNAMIC WHEN ADDING CONTROLLER UI

    if track_id == "Track-1":

        waypoints = [
            Waypoint(12.9716, 80.1480),
            Waypoint(12.9750, 80.1550),
            Waypoint(12.9800, 80.1650),
            Waypoint(12.9900, 80.1800),
        ]

        return TrackModel(waypoints)
    
    if track_id == "Track-2":

        waypoints = [
            Waypoint(12.99, 80.24),
            Waypoint(12.27, 79.006),
            Waypoint(9.93, 78.06),
            Waypoint(8.15, 77.42),
        ]

        return TrackModel(waypoints)

    # Can add other tracks similarly here for now .. later can be added dynamically

