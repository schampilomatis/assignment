import requests
import base64
from django.conf import settings
import json


class NotificareManager(object):
    PAYLOAD_DATA = {
        "type": "re.notifica.notification.Alert",
        "schedule": False,
        "content": [
            {
                "type": "re.notifica.content.Text",
                "data": "test"
            }
        ]
    }

    AUTHORIZATION = base64.encodestring('%s:%s' % (settings.NOTIFICARE_KEY, settings.NOTIFICARE_MASTER_SECRET)).replace(
        '\n', '')

    HEADERS = {
        'Authorization': "Basic %s" % AUTHORIZATION,
        'Content-Type': 'application/json',
    }

    URL = 'https://push.notifica.re/notification/{}'

    @classmethod
    def send_notification_by_user(cls, user_id, message, extra=None):
        if not extra:
            extra = {}
        data = dict(cls.PAYLOAD_DATA, message=message, extra=extra)
        url = cls.URL.format('user/' + user_id)
        request = requests.post(url, data=json.dumps(data), headers=cls.HEADERS)

        if request.ok:
            return True

        return False


    @classmethod
    def send_notification_to_all(cls, message, extra={}):
        data = dict(cls.PAYLOAD_DATA, message=message, extra=extra)
        url = cls.URL.format('broadcast')
        request = requests.post(url, data=json.dumps(data), headers=cls.HEADERS)
        if request.ok:
            return True
        return False
