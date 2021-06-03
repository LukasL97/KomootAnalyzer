import click
from tqdm import tqdm

from src.main.client.KomootClient import KomootClient


@click.command()
@click.option('--email')
@click.option('--password')
@click.option('--tour_type', default='tour_recorded')
@click.option('--sport_types', default='touringbicycle,racebike')
@click.option('--output_dir')
def main(email, password, tour_type, sport_types, output_dir):
    client = KomootClient()
    user_id = client.login(email, password)
    tours = client.get_tours(user_id, tour_type=tour_type, sport_types=sport_types.split(','))
    for tour in tqdm(tours):
        gpx = client.get_gpx(tour['id'])
        with open(f'{output_dir}/{tour["id"]}.gpx', 'w+') as gpx_file:
            gpx_file.write(gpx)


if __name__ == '__main__':
    main()
