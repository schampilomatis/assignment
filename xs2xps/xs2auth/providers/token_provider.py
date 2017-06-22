from __future__ import absolute_import
from ..models import ExpiringToken as Token
from django.core.exceptions import ObjectDoesNotExist


class TokenProvider(object):
    @classmethod
    def authenticate(cls, header_array):
        try:
            key = header_array[1]
            token = Token.objects.select_related('user').get(key=key)

        except ObjectDoesNotExist:
            return None

        if token.expired():
            return None

        if not token.user.is_active:
            return None
        return token.user, token
