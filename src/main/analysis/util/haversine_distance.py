from typing import List

from gpxpy.gpx import GPXTrackPoint
from haversine import haversine, Unit


def distance(a: GPXTrackPoint, b: GPXTrackPoint) -> float:
    return haversine(
        (a.latitude, a.longitude),
        (b.latitude, b.longitude),
        Unit.METERS
    )


def section_length(section: List[GPXTrackPoint]) -> float:
    last_point = section[0]
    length = 0
    for point in section[1:]:
        length += distance(last_point, point)
        last_point = point
    return length
