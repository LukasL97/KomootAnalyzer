import os

import click
from tqdm import tqdm

from src.main.analysis.tour_novelty import extract_novelty_sections
from src.main.analysis.util.haversine_distance import section_length
from src.main.model.Tour import Tour
from src.main.util.list_helpers import flatten


def get_tours(tour_dir):
    tours = []
    for tour_file in tqdm(os.listdir(tour_dir), desc='Load gpx files'):
        with open(f'{tour_dir}/{tour_file}', 'r') as gpx_file:
            tours.append(Tour(gpx_file.read()))
    return sorted(tours, key=lambda tour: tour.date)


def get_novelty_distances(tours, threshold):
    previous_points = []
    novelty_distances = []
    for tour in tqdm(tours, desc='Calculate novelty distances'):
        novelty_sections = extract_novelty_sections(previous_points, tour.points, threshold)
        novelty_distance = sum(section_length(section) for section in novelty_sections)
        novelty_distances.append(novelty_distance)
        previous_points += flatten(novelty_sections)
    return novelty_distances


@click.command()
@click.option('--tour_dir')
@click.option('--threshold', default=50)
def main(tour_dir, threshold):
    tours = get_tours(tour_dir)
    get_novelty_distances(tours, threshold)



if __name__ == '__main__':
    main()