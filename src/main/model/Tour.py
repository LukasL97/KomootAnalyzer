from __future__ import annotations

from datetime import datetime
from typing import List, Optional

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
        points: List[GPXTrackPoint],
        novelties: Optional[List[List[GPXTrackPoint]]]
    ):
        self.id: str = id
        self.user: str = user
        self.name: str = name
        self.date: datetime = date
        self.points: List[GPXTrackPoint] = points
        self.novelties: Optional[List[List[GPXTrackPoint]]] = novelties

    @classmethod
    def from_gpx(cls, id: str, user: str, gpx: str) -> Tour:
        gpx = gpxpy.parse(gpx)
        return cls(
            id,
            user,
            gpx.tracks[0].name,
            gpx.tracks[0].segments[0].points[0].time,
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
