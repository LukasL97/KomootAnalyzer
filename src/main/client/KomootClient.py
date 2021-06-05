import json
import logging
import re
from typing import Optional, List, Dict, Any

from requests import Session


class KomootClient:

    def __init__(self, cookies: Optional[Dict[str, str]] = None):
        self.session = Session()
        if cookies:
            for key, value in cookies.items():
                self.session.cookies.set(key, value)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.debug(f'Set cookies: {self.get_cookies()}')

    def get_cookies(self) -> Dict[str, str]:
        return self.session.cookies.get_dict()

    def login(self, email: str, password: str) -> str:
        self.logger.info(f'Execute komoot login for email {email}')
        login_response = self.session.post(
            'https://account.komoot.com/v1/signin',
            json={
                'email': email,
                'password': password
            },
            headers={
                'Content-Type': 'application/json'
            }
        )
        assert login_response.status_code == 200
        transfer_response = self.session.get('https://account.komoot.com/actions/transfer?type=signin')
        user_id = re.search('user/([0-9]+)/tours', transfer_response.text).group(1)
        self.logger.info(f'Received user id {user_id} for email {email}')
        return user_id

    def get_tours(
        self,
        user_id: str,
        limit: int = 10000,
        tour_type: Optional[str] = None,
        sport_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        self.logger.info(f'Fetch tours for user with id {user_id}')
        tours_url = f'https://www.komoot.de/api/v007/users/{user_id}/tours/?limit={limit}'
        if tour_type:
            tours_url += f'&type={tour_type}'
        if sport_types:
            sport_types_str = ','.join(sport_types)
            tours_url += f'&sport_types={sport_types_str}'
        tours_response = self.session.get(tours_url)
        self.logger.info(f'Received response code {tours_response.status_code}')
        tours = json.loads(tours_response.text)['_embedded']['tours']
        self.logger.info(f'Retrieved {len(tours)} for user with id {user_id}')
        return tours

    def get_gpx(self, tour_id: str) -> str:
        self.logger.info(f'Download gpx for tour with id {tour_id}')
        gpx_response = self.session.get(f'https://www.komoot.de/api/v007/tours/{tour_id}.gpx')
        self.logger.info(f'Received response code {gpx_response.status_code}')
        return gpx_response.text
