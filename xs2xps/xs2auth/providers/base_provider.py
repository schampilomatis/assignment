from django.contrib.auth import get_user_model
from abc import ABCMeta, abstractmethod
from rest_framework.exceptions import APIException
User = get_user_model()


class BaseProvider(object):

    __metaclass__ = ABCMeta

    @classmethod
    def authenticate(cls, header, user_provider_id):

        try:
            username, data = cls._get_info(header[1])
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = User()
            user.username = username
            user.provider = cls.name
        #     TODO FIX EXCEPTION HANDLING HERE (WITH LOGGING)
        # except BaseException:
        #     raise CustomException(ERROR_CODES.INVALID_TOKEN, 403)

        cls._set_data(data, user)
        if user.provider_id != user_provider_id:
            raise APIException('PARAMS_INCORRECT', 403)

        user.save()
        return user, None

    # sets data to user
    @classmethod
    @abstractmethod
    def _set_data(cls, data, user): pass


    # has to return tuple (email, data)
    @classmethod
    @abstractmethod
    def _get_info(cls, header): pass


    @classmethod
    def _get_provider_alternative(cls, id):
        if id:
            return cls.name + str(id)
        return None

    @classmethod
    def _get_first_not_null(self, usernames):
        for username in usernames:
            if username:
                return username
        raise APIException('AUTHENTICATION_DATA_NOT_VALID', 403)


