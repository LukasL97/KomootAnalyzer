from typing import List, Optional

from gpxpy.geo import LocationDelta
from gpxpy.gpx import GPXTrackPoint

from src.main.analysis.util.haversine_distance import distance


def extract_novelty_sections(
    previous_tour_points: List[GPXTrackPoint],
    new_tour_points: List[GPXTrackPoint],
    min_novelty_distance: float
) -> List[List[GPXTrackPoint]]:
    relevant_previous_tour_points = filter_relevant_previous_tour_points(
        previous_tour_points,
        new_tour_points,
        min_novelty_distance
    )
    print(f'reduced {len(previous_tour_points)} to {len(relevant_previous_tour_points)} points')
    novelty_sections = []
    active_novelty_section: Optional[List[GPXTrackPoint]] = None
    for idx, new_tour_point in enumerate(new_tour_points):
        near_previous_tour_points = [
            point for point in relevant_previous_tour_points if
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
    return novelty_sections


def filter_relevant_previous_tour_points(
    previous_tour_points: List[GPXTrackPoint],
    new_tour_points: List[GPXTrackPoint],
    min_novelty_distance: float
) -> List[GPXTrackPoint]:
    relevant_previous_tour_points = []
    bounding_box_left = min(
        (point + LocationDelta(min_novelty_distance, LocationDelta.WEST)).longitude for point in new_tour_points)
    bounding_box_right = max(
        (point + LocationDelta(min_novelty_distance, LocationDelta.EAST)).longitude for point in new_tour_points)
    bounding_box_top = max(
        (point + LocationDelta(min_novelty_distance, LocationDelta.NORTH)).latitude for point in new_tour_points)
    bounding_box_bottom = min(
        (point + LocationDelta(min_novelty_distance, LocationDelta.SOUTH)).latitude for point in new_tour_points)
    for previous_tour_point in previous_tour_points:
        if not (previous_tour_point.longitude < bounding_box_left
                or previous_tour_point.longitude > bounding_box_right
                or previous_tour_point.latitude > bounding_box_top
                or previous_tour_point.latitude < bounding_box_bottom):
            for new_tour_point in new_tour_points:
                if distance(previous_tour_point, new_tour_point) < min_novelty_distance:
                    relevant_previous_tour_points.append(previous_tour_point)
                    break
    return relevant_previous_tour_points
