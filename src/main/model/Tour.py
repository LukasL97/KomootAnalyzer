from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Dict, Any

import gpxpy
from gpxpy.gpx import GPXTrackPoint

from src.main.analysis.tour_novelty import extract_novelty_sections
from src.main.analysis.util.haversine_distance import section_length


class Tour:

    def __init__(
        self,
        id: str,
        user: str,
        name: str,
        date: datetime,
        distance: float,
        duration: int,
        time_in_motion: int,
        elevation_up: float,
        elevation_down: float,
        points: List[GPXTrackPoint],
        novelties: Optional[List[List[GPXTrackPoint]]]
    ):
        self.id: str = id
        self.user: str = user
        self.name: str = name
        self.date: datetime = date
        self.distance = distance
        self.duration = duration
        self.time_in_motion = time_in_motion
        self.elevation_up = elevation_up
        self.elevation_down = elevation_down
        self.points: List[GPXTrackPoint] = points
        self.novelties: Optional[List[List[GPXTrackPoint]]] = novelties

    @classmethod
    def from_komoot(cls, user: str, komoot_tour: Dict[str, Any], gpx: str) -> Tour:
        gpx = gpxpy.parse(gpx)
        return cls(
            komoot_tour['id'],
            user,
            gpx.tracks[0].name,
            gpx.tracks[0].segments[0].points[0].time,
            komoot_tour['distance'],
            komoot_tour['duration'],
            komoot_tour['time_in_motion'],
            komoot_tour['elevation_up'],
            komoot_tour['elevation_down'],
            gpx.tracks[0].segments[0].points,
            None
        )

    def distance(self) -> float:
        return section_length(self.points)

    def novelty_distance(self) -> float:
        if self.novelties:
            return sum(section_length(novelty) for novelty in self.novelties)
        else:
            return 0


    def set_novelties(self, previous_tours: List[Tour], min_novelty_distance: float):
        previous_tour_points = [point for tour in previous_tours for novelty in tour.novelties for point in novelty]
        self.novelties = extract_novelty_sections(previous_tour_points, self.points, min_novelty_distance)
