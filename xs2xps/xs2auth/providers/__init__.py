from facebook_provider import FacebookProvider
from token_provider import TokenProvider
from linkedin_provider import LinkedInProvider
from google_provider import GoogleProvider

_AVAILABLE_PROVIDERS = {
    'local': TokenProvider,
    'facebook': FacebookProvider,
    'linkedin': LinkedInProvider,
    'google': GoogleProvider
}

def get_provider(provider_key):
    if provider_key == 'local':
        return None
    return _AVAILABLE_PROVIDERS.get(provider_key.lower())

def get_local_provider():
    return _AVAILABLE_PROVIDERS['local']