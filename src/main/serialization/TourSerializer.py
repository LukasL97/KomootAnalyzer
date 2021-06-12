from typing import Dict, Any

from gpxpy.gpx import GPXTrackPoint

from src.main.model.Tour import Tour


class TourSerializer:

    @classmethod
    def serialize(cls, tour: Tour) -> Dict[str, Any]:
        return {
            'id': tour.id,
            'user': tour.user,
            'name': tour.name,
            'date': tour.date,
            'distance': tour.distance,
            'duration': tour.duration,
            'time_in_motion': tour.time_in_motion,
            'elevation_up': tour.elevation_up,
            'elevation_down': tour.elevation_down,
            'points': [cls.serialize_point(point) for point in tour.points],
            'novelties': [
                [cls.serialize_point(point) for point in novelty] for novelty in tour.novelties
            ] if tour.novelties is not None else None
        }

    @classmethod
    def serialize_point(cls, point: GPXTrackPoint) -> Dict[str, Any]:
        return {
            'latitude': point.latitude,
            'longitude': point.longitude,
            'elevation': point.elevation,
            'time': point.time
        }

    @classmethod
    def deserialize(cls, tour: Dict[str, Any]) -> Tour:
        return Tour(
            tour['id'],
            tour['user'],
            tour['name'],
            tour['date'],
            tour['distance'],
            tour['duration'],
            tour['time_in_motion'],
            tour['elevation_up'],
            tour['elevation_down'],
            [cls.deserialize_point(point) for point in tour['points']],
            [
                [cls.deserialize_point(point) for point in novelty] for novelty in tour['novelties']
            ] if tour['novelties'] is not None else None
        )

    @classmethod
    def deserialize_point(cls, point: Dict[str, Any]) -> GPXTrackPoint:
        return GPXTrackPoint(
            point['latitude'],
            point['longitude'],
            point['elevation'],
            point['time']
        )
