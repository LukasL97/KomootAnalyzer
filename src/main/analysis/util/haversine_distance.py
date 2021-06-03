from gpxpy.gpx import GPXTrackPoint
from haversine import haversine, Unit


def distance(a: GPXTrackPoint, b: GPXTrackPoint):
    return haversine(
        (a.latitude, a.longitude),
        (b.latitude, b.longitude),
        Unit.METERS
    )
