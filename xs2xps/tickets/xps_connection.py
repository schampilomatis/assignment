from zeep import Client
from zeep.helpers import serialize_object
from django.conf import settings
WSDL = 'https://secure.xpslogic.com/service/{}/{}.wsdl'


class XPSClient(object):
    clients = {}
    header = {"parameters": {"token": settings.XPS_TOKEN}}

    @classmethod
    def _get_service(cls, service):
        if not cls.clients.get(service):
            cls.clients[service] = Client(WSDL.format(settings.XPS_ACCOUNT, service))
        return cls.clients[service]

    @classmethod
    def call_action(cls, service, action, params={}):
        return serialize_object(getattr(cls._get_service(service).service, action)(_soapheaders=cls.header, **params))
