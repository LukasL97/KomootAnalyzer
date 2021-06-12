import click

from src.main.client.KomootClient import KomootClient
from src.main.dao.ToursDAO import ToursDAO


@click.command()
@click.option('--email')
@click.option('--password')
def main(email, password):
    client = KomootClient()
    user_id = client.login(email, password)
    komoot_tours = client.get_tours(user_id, tour_type='tour_recorded', sport_types=['touringbicycle', 'racebike'])
    for komoot_tour in komoot_tours:
        db_tour = ToursDAO.collection.find_one({'id': komoot_tour['id']})
        if db_tour is None:
            print(f'Skip tour with id {komoot_tour["id"]} which is not in the DB')
        else:
            new_values = {
                'distance': komoot_tour['distance'],
                'duration': komoot_tour['duration'],
                'time_in_motion': komoot_tour['time_in_motion'],
                'elevation_up': komoot_tour['elevation_up'],
                'elevation_down': komoot_tour['elevation_down']
            }
            ToursDAO.collection.update_one(
                {'id': komoot_tour['id']},
                {'$set': new_values}
            )

if __name__ == '__main__':
    main()