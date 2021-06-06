from __future__ import annotations

import logging
from typing import Any, Dict, List

from pykka import ThreadingActor

from src.main.client.KomootClient import KomootClient
from src.main.dao.ToursDAO import ToursDAO
from src.main.model.Tour import Tour


class ToursUpdateWorker(ThreadingActor):

    def __init__(self, user_id: str):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.user_id = user_id
        super().__init__()

    def on_receive(self, message: Any) -> Any:
        if isinstance(message, ToursUpdateMessage):
            self.execute_update(message)
        else:
            self.logger.error(RuntimeError(f'{self.__class__.__name__} received unexpected message {str(message)}'))

    def execute_update(self, message: ToursUpdateMessage):
        self.logger.info(f'Execute tours update for user with id {message.session_cookies["komoot_user_id"]}')
        client = KomootClient(cookies=message.session_cookies)
        user_id = message.session_cookies['komoot_user_id']
        komoot_tours = client.get_tours(user_id, tour_type='tour_recorded', sport_types=['touringbicycle', 'racebike'])
        komoot_tour_ids = [tour['id'] for tour in komoot_tours]
        db_tours = ToursDAO.find_by_user(user_id)
        db_tour_ids = [tour.id for tour in db_tours]
        komoot_tour_ids_not_in_db = [id for id in komoot_tour_ids if not id in db_tour_ids]
        self.logger.info(f'Found {len(komoot_tour_ids_not_in_db)} tours missing in DB')
        komoot_tours_not_in_db = []
        for id in komoot_tour_ids_not_in_db:
            gpx = client.get_gpx(id)
            komoot_tours_not_in_db.append(Tour.from_gpx(id, user_id, gpx))
        self.update_db_with_novelties(db_tours, komoot_tours_not_in_db)
        self.logger.info(f'Stop worker')
        self.stop()

    def update_db_with_novelties(self, db_tours: List[Tour], new_tours: List[Tour]):
        self.logger.info(f'Update DB with {len(new_tours)} new tours')
        db_tours.sort(key=lambda tour: tour.date)
        new_tours.sort(key=lambda tour: tour.date)
        for tour in db_tours:
            assert tour.novelties is not None
        previous_tours = db_tours.copy()
        for tour in new_tours:
            self.logger.info(f'Set novelties for tour with id {tour.id}')
            tour.set_novelties(previous_tours, min_novelty_distance=50)
            ToursDAO.insert_one(tour)
            previous_tours.append(tour)


class ToursUpdateMessage:

    def __init__(self, session_cookies: Dict[str, str]):
        self.session_cookies = session_cookies
