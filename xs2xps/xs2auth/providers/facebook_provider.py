from base_provider import BaseProvider
import facebook


class FacebookProvider(BaseProvider):

    name = 'facebook'

    @classmethod
    def _set_data(cls, facebook_info, user):
        user.email = facebook_info.get('email')
        user.name = facebook_info.get('first_name')
        user.lastname = facebook_info.get('last_name')
        user.provider_id = facebook_info.get('id')

    @classmethod
    def _get_info(cls, facebook_token):
        graph = facebook.GraphAPI(facebook_token)
        facebook_info = graph.get_object("me", fields="id,name,email,first_name,last_name")
        username = cls._get_first_not_null([facebook_info.get('email'), cls._get_provider_alternative(facebook_info.get('id'))])
        return username, facebook_info
