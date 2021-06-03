from typing import List, Optional

from gpxpy.gpx import GPXTrackPoint

from src.main.analysis.util.haversine_distance import distance


def calculate_novelty_distance(
    previous_tour_points: List[GPXTrackPoint],
    new_tour_points: List[GPXTrackPoint],
    min_novelty_distance: float
) -> float:
    novelty_sections = []
    active_novelty_section: Optional[List[GPXTrackPoint]] = None
    for idx, new_tour_point in enumerate(new_tour_points):
        near_previous_tour_points = [
            point for point in previous_tour_points if
            distance(point, new_tour_point) < min_novelty_distance
        ]
        if len(near_previous_tour_points):
            if active_novelty_section:
                active_novelty_section.append(new_tour_point)
                novelty_sections.append(active_novelty_section)
                active_novelty_section = None
        else:
            if active_novelty_section:
                active_novelty_section.append(new_tour_point)
            else:
                active_novelty_section = [] if idx == 0 else [new_tour_points[idx - 1]]
                active_novelty_section.append(new_tour_point)
    if active_novelty_section:
        novelty_sections.append(active_novelty_section)
    overall_novelty_distance = 0
    for novelty_section in novelty_sections:
        section_novelty_distance = 0
        last_point = novelty_section[0]
        for point in novelty_section[1:]:
            section_novelty_distance += distance(last_point, point)
            last_point = point
        overall_novelty_distance += section_novelty_distance
    return overall_novelty_distance
