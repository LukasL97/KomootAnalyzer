from typing import List, Dict, Any, Optional

from gpxpy.gpx import GPXTrackPoint

from src.main import mongo
from src.main.model.Tour import Tour


class ToursDAO:
    collection = mongo.db.get_collection('Tours')

    @classmethod
    def insert_one(cls, tour: Tour):
        cls.collection.insert_one(ToursSerializer.serialize(tour))

    @classmethod
    def insert_many(cls, tours: List[Tour]):
        cls.collection.insert_many([ToursSerializer.serialize(tour) for tour in tours])

    @classmethod
    def update(cls, tour: Tour):
        delete_result = cls.collection.delete_one({'id': tour.id})
        if delete_result.deleted_count > 0:
            cls.insert_one(tour)
        else:
            raise RuntimeError(f'Tried updating tour with id {tour.id} but could not find it in DB')

    @classmethod
    def find_by_id(cls, id: str) -> Optional[Tour]:
        tour = cls.collection.find_one({'id': id})
        return ToursSerializer.deserialize(tour) if tour else None

    @classmethod
    def find_by_user(cls, user: str) -> List[Tour]:
        tours = cls.collection.find({'user': user})
        return [ToursSerializer.deserialize(tour) for tour in tours]


class ToursSerializer:

    @classmethod
    def serialize(cls, tour: Tour) -> Dict[str, Any]:
        return {
            'id': tour.id,
            'user': tour.user,
            'name': tour.name,
            'date': tour.date,
            'points': [cls.serialize_point(point) for point in tour.points],
            'novelties': [
                [cls.serialize_point(point) for point in novelty] for novelty in tour.novelties
            ] if tour.novelties else None
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
            [cls.deserialize_point(point) for point in tour['points']],
            [
                [cls.deserialize_point(point) for point in novelty] for novelty in tour['novelties']
            ] if tour['novelties'] else None
        )

    @classmethod
    def deserialize_point(cls, point: Dict[str, Any]) -> GPXTrackPoint:
        return GPXTrackPoint(
            point['latitude'],
            point['longitude'],
            point['elevation'],
            point['time']
        )
