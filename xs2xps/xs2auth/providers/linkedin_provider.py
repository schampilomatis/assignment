from base_provider import BaseProvider
import requests
import xmltodict


class LinkedInProvider(BaseProvider):

    name = 'linkedin'

    @classmethod
    def _set_data(cls, linkedin_data, user):
        user.email = linkedin_data['person'].get('email-address')
        user.name = linkedin_data['person'].get('first-name')
        user.lastname = linkedin_data['person'].get('last-name')
        user.provider_id = linkedin_data['person'].get('id')

    @classmethod
    def _get_info(cls, linkedin_token):
        url = "https://api.linkedin.com/v1/people/~:(id,first-name,last-name,picture-url,public-profile-url,email-address)?oauth2_access_token={}".format(
            linkedin_token)
        response = requests.get(url)
        linkedin_data = xmltodict.parse(response.content)
        username = cls._get_first_not_null([linkedin_data['person'].get('email-address'), cls._get_provider_alternative(linkedin_data['person'].get('id'))])
        return username, linkedin_data
