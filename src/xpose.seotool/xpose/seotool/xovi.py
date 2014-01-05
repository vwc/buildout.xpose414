import socket
import contextlib
try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
from urllib2 import HTTPError
from five import grok
from plone import api
from zope.interface import Interface
from zope.component import getMultiAdapter


DEFAULT_SERVICE_URI = 'https://api.xovi.net/index.php?'
DEFAULT_SERVICE_TIMEOUT = socket.getdefaulttimeout()


class IXoviTool(Interface):
    """ Api call processing and session data storage """

    def status(context):
        """ Check availability of Xovi api

        @param timeout: Set status request timeout
        """

    def get_config(context):
        """ Get XOVI api records from configuration registry

        @param record: Specify desired record type e.g. client_key
        """


class XoviTool(grok.GlobalUtility):
    grok.provides(IXoviTool)

    def status(self, timeout=DEFAULT_SERVICE_TIMEOUT):
        service_url = self.get_config('api_uri')
        service_key = self.get_config('client_key')
        params = xovi_request_base()
        params['method'] = u'getCreditState'
        params['key'] = service_key
        url = service_url + '?' + urlencode(params)
        with contextlib.closing(urlopen(url)) as response:
            response = response.read().decode('utf-8')
        return response

    def get_config(self, record=None):
        record_key = 'xeo.cxn.xovi_{0}'.format(record)
        record = api.portal.get_registry_record(record_key)
        return record


def xovi_request_base():
    parameters = {
        'service': u'user',
        'format':  u'json',
    }
    return parameters
