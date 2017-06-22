from base_provider import BaseProvider
import json
import requests


class GoogleProvider(BaseProvider):

    name = 'google'

    @classmethod
    def _set_data(cls, google_data, user):
        user.email = google_data.get('email')
        user.name = google_data.get('given_name')
        user.lastname = google_data.get('family_name')
        user.provider_id = google_data.get('id')

    @classmethod
    def _get_info(cls, google_token):
        url = 'https://www.googleapis.com/oauth2/v1/userinfo'
        headers = {"Authorization":"Bearer {}".format(google_token)}
        google_response = requests.get(url, headers=headers)
        google_info = json.loads(google_response.text)
        username = cls._get_first_not_null([google_info.get('email'), cls._get_provider_alternative(google_info.get('id'))])
        return username, google_info
