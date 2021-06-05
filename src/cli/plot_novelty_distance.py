import click

from src.main.client.KomootClient import KomootClient
from src.main.dao.ToursDAO import ToursDAO

import pandas as pd
import matplotlib.pyplot as plt


@click.command()
@click.option('--email')
@click.option('--password')
def main(email, password):
    client = KomootClient()
    user_id = client.login(email, password)
    tours = ToursDAO.find_by_user(user_id)
    print(f'Found {len(tours)} tours for this user')
    data = pd.DataFrame([{
        'date': tour.date,
        'distance': tour.distance() / 1000,
        'novelty': tour.novelty_distance() / 1000
    } for tour in tours])
    monthly_data = data.groupby(data['date'].dt.to_period('M')).sum()
    monthly_data = monthly_data.resample('M').asfreq().fillna(0)
    monthly_data.plot(kind='bar')
    plt.show()


if __name__ == '__main__':
    main()
