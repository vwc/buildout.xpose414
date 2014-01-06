import json
import socket
import contextlib
from urllib import urlencode
from urllib2 import urlopen
from urllib2 import HTTPError
from five import grok
from plone import api
from zope.interface import Interface


DEFAULT_SERVICE_URI = 'http://brain.xpose414.de/public/api.php'
DEFAULT_SERVICE_TIMEOUT = socket.getdefaulttimeout()


class IACTool(Interface):
    """ API call processing and session data storage """

    def status(context):
        """ Check availability of Active Collab api

        @param timeout: Set status request timeout
        """

    def get_config(context):
        """ Get Active Collab api records from configuration registry

        @param record: Specify desired record type e.g. client_key
        """


class ACTool(grok.GlobalUtility):
    grok.provides(IACTool)

    def status(self, timeout=DEFAULT_SERVICE_TIMEOUT):
        info = {}
        info['name'] = 'activeCollab'
        service_url = self.get_config('api_uri')
        params = {
            'check_if_alive':  '1',
        }
        url = service_url + '?' + urlencode(params)
        try:
            with contextlib.closing(urlopen(url)) as response:
                response = response.read().decode('utf-8')
            info['code'] = '0'
            info['status'] = u'Ok'
            info['response'] = 'API is alive'
        except HTTPError:
            info['code'] = '1'
            info['status'] = u'Not available'
            info['response'] = 'API is not available'
        return info

    def make_request(self, path_info=u'info',
                     timeout=DEFAULT_SERVICE_TIMEOUT):
        service_url = self.get_config('api_uri')
        service_key = self.get_config('client_key')
        params = ac_request_base()
        params['path_info'] = path_info
        params['auth_api_token'] = service_key
        url = service_url + '?' + urlencode(params)
        with contextlib.closing(urlopen(url)) as response:
            response = response.read().decode('utf-8')
        res = json.loads(response)
        return res

    def get_config(self, record=None):
        record_key = 'xeo.cxn.ac_{0}'.format(record)
        record = api.portal.get_registry_record(record_key)
        return record


def ac_request_base():
    parameters = {
        'format':  u'json',
    }
    return parameters
