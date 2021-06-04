from unittest import TestCase

from gpxpy.gpx import GPXTrackPoint

from src.main.analysis.tour_novelty import extract_novelty_sections


class TourNoveltyTest(TestCase):

    def test_calculate_novelty_distance(self):
        previous_tour_points = [
            GPXTrackPoint(latitude=50.0641997714135, longitude=8.452668902092038),
            GPXTrackPoint(latitude=50.054942549611795, longitude=8.452840563462125),
            GPXTrackPoint(latitude=50.04617960508518, longitude=8.464084383202932),
            GPXTrackPoint(latitude=50.05141551906473, longitude=8.484769578298618),
            GPXTrackPoint(latitude=50.06293251919943, longitude=8.485284562408882),
            GPXTrackPoint(latitude=50.07317977341163, longitude=8.49532675255907),
            GPXTrackPoint(latitude=50.06998462797887, longitude=8.515840286284666),
            GPXTrackPoint(latitude=50.05714681205976, longitude=8.518758529576173),
        ]
        new_tour_points = [
            GPXTrackPoint(latitude=50.0641997714135, longitude=8.452668902092038),
            GPXTrackPoint(latitude=50.054942549611795, longitude=8.452840563462125),
            GPXTrackPoint(latitude=50.058799942441915, longitude=8.46442770594311),
            GPXTrackPoint(latitude=50.06023260936559, longitude=8.473611589242854),
            GPXTrackPoint(latitude=50.06293251919943, longitude=8.485284562408882),
            GPXTrackPoint(latitude=50.061940733244214, longitude=8.495755905984293),
            GPXTrackPoint(latitude=50.06028771108519, longitude=8.50820135531572),
            GPXTrackPoint(latitude=50.05714681205976, longitude=8.518758529576173),
        ]
        self.assertEqual(
            extract_novelty_sections(previous_tour_points, new_tour_points, 50),
            [new_tour_points[1:5], new_tour_points[4:8]]
        )
