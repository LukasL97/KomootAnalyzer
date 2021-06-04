from typing import List

import gpxpy
from gpxpy.gpx import GPXTrackPoint

from src.main.analysis.util.haversine_distance import distance


class Tour:

    def __init__(self, gpx: str):
        self.gpx = gpxpy.parse(gpx)
        self.name = self.gpx.tracks[0].name
        self.date = self.gpx.tracks[0].segments[0].points[0].time.date()

    def get_points(self) -> List[GPXTrackPoint]:
        return self.gpx.tracks[0].segments[0].points

    def distance(self) -> float:
        points = self.get_points()
        last_point = points[0]
        overall_distance = 0
        for point in points[1:]:
            overall_distance += distance(last_point, point)
            last_point = point
        return overall_distance
