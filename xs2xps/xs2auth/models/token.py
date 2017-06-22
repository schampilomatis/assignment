from rest_framework.authtoken.models import Token
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

# TODO: Should we refresh token after a normal login? should we add refresh token?
class ExpiringToken(Token):

    """Extend Token to add an expired method."""
    class Meta(object):
        proxy = True

    #change this for normal tokens
    expires = True

    @property
    def token_lifespan(self):
        try:
            return settings.TOKEN_LIFESPAN
        except AttributeError:
            return timezone.timedelta(days=30)

    def expired(self):
        if not self.expires:
            return False
        now = timezone.now()
        if self.created < now - self.token_lifespan:
            return True
        return False

    @classmethod
    def get_or_create_if_expired(cls, user):
        try:
            token = cls.objects.get(user=user)
        except ObjectDoesNotExist:
            return cls.objects.create(user=user)

        if token.expired():
            token.delete()
            return cls.objects.create(user=user)

        return token