import math
from typing import List
from tracking.waypoint import Waypoint


def haversine(lat1, lon1, lat2, lon2): # To cslculate distance in meters between two GPS points.

    R = 6371000  # Approx earth radius in meters

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2 +
        math.cos(phi1) *
        math.cos(phi2) *
        math.sin(dlambda / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c


class TrackModel:   # CLASS DEFINING THE STRUCTURE OF A TRACK WHICH IS BUILT USING VARIOUS WAYPOINTS 

    def __init__(self, waypoints: List[Waypoint]):
        self.waypoints = waypoints
        self.cumulative_distances = []
        self.total_length = 0.0

        self._compute_distances()

    def _compute_distances(self):
        self.cumulative_distances = [0.0]

        total = 0.0

        for i in range(1, len(self.waypoints)):
            wp1 = self.waypoints[i - 1]
            wp2 = self.waypoints[i]

            d = haversine(wp1.lat, wp1.lon, wp2.lat, wp2.lon)
            total += d
            self.cumulative_distances.append(total)

        self.total_length = total

    def get_coordinates(self, position_m: float):

        if position_m <= 0:
            wp = self.waypoints[0]
            return wp.lat, wp.lon

        if position_m >= self.total_length:
            wp = self.waypoints[-1]
            return wp.lat, wp.lon

        for i in range(1, len(self.cumulative_distances)):

            if position_m <= self.cumulative_distances[i]:

                wp1 = self.waypoints[i - 1]
                wp2 = self.waypoints[i]

                segment_start = self.cumulative_distances[i - 1]
                segment_end = self.cumulative_distances[i]

                segment_length = segment_end - segment_start
                segment_position = position_m - segment_start

                ratio = segment_position / segment_length

                lat = wp1.lat + ratio * (wp2.lat - wp1.lat)
                lon = wp1.lon + ratio * (wp2.lon - wp1.lon)

                return lat, lon

        wp = self.waypoints[-1]
        return wp.lat, wp.lon

