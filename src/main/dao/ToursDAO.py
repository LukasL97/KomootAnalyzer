from typing import List, Optional

from src.main import mongo
from src.main.model.Tour import Tour
from src.main.serialization.TourSerializer import TourSerializer


class ToursDAO:
    collection = mongo.db.get_collection('Tours')

    @classmethod
    def insert_one(cls, tour: Tour):
        cls.collection.insert_one(TourSerializer.serialize(tour))

    @classmethod
    def insert_many(cls, tours: List[Tour]):
        cls.collection.insert_many([TourSerializer.serialize(tour) for tour in tours])

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
        return TourSerializer.deserialize(tour) if tour else None

    @classmethod
    def find_by_user(cls, user: str) -> List[Tour]:
        tours = cls.collection.find({'user': user})
        return [TourSerializer.deserialize(tour) for tour in tours]
