from __future__ import absolute_import
import base64
from rest_framework.exceptions import APIException
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from .providers import get_provider, get_local_provider
from .models import ExpiringToken as Token
User = get_user_model()
import json

class CustomBasicAuthentication(BaseAuthentication):
    """
    HTTP Basic authentication against username/password.
    """
    www_authenticate_realm = 'api'

    def authenticate(self, request):
        """
        Returns a `User` if a correct username and password have been supplied
        using HTTP Basic authentication.  Otherwise returns `None`.
        """
        auth_header = get_authorization_header(request).split()
        if not auth_header or auth_header[0].lower() != b'basic':
            return None

        if len(auth_header) != 2:
            raise APIException('INVALID_AUTH_HEADER', 403)

        try:
            auth_parts = base64.b64decode(auth_header[1]).decode(HTTP_HEADER_ENCODING).partition(':')
        except (TypeError, UnicodeDecodeError):
            raise APIException('INVALID_AUTH_HEADER', 403)

        username, password = auth_parts[0], auth_parts[2]
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise APIException('USER_DOES_NOT_EXIST', 403)
        return self.authenticate_credentials(user.username, password)

    def authenticate_credentials(self, username, password):
        """
        Authenticate the userid and password against username and password.
        """
        user = authenticate(username=username, password=password)
        if user is None or not user.is_active:
            raise APIException('INACTIVE_USER', 403)
        Token.get_or_create_if_expired(user=user)
        return (user, None)

    def authenticate_header(self, request):
        return 'Basic realm="%s"' % self.www_authenticate_realm


class ProviderAuthentication(BaseAuthentication):
    """
    Simple token based authentication.

    Clients should authenticate by passing the token key in the "Authorization"
    HTTP header, prepended with the string "{Provider} " (case insensitive).
    Check options in providers/util.py  For example:

        Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
        Authorization: FBToken 401f7ac837da42b97f613d789819ff93537bee6a
    """

    def authenticate(self, request):
        auth_header = get_authorization_header(request).split()

        if not auth_header:
            return None

        if auth_header[0].lower() != 'token':
            return None

        if len(auth_header) != 2:
            raise APIException('INVALID_AUTH_HEADER', 403)

        try:
            data = json.loads(request.body)
        except ValueError:
            raise APIException('JSON_INVALID', 403)

        try:
            id = data['user_provider_id']
            provider = data['provider']
        except KeyError:
            raise APIException('PARAMS_MISSING', 403)

        provider = get_provider(provider)
        if not provider:
            return None

        return provider.authenticate(auth_header, id)


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = get_authorization_header(request).split()

        if not auth_header:
            return None

        if len(auth_header) != 2:
            raise APIException('INVALID_AUTH_HEADER', 403)

        if auth_header[1].lower() != 'token':
            return None

        provider = get_local_provider()
        return provider.authenticate(auth_header)
