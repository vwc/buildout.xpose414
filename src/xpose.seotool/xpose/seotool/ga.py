import socket
import httplib2
from five import grok
from plone import api
from zope.interface import Interface
from oauth2client.client import OAuth2WebServerFlow
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

DEFAULT_SERVICE_TIMEOUT = socket.getdefaulttimeout()


class IGATool(Interface):
    """ API call processing and session data storage """


class GATool(grok.GlobalUtility):
    grok.provides(IGATool)

    def get_config(self, record=None):
        record_key = 'xeo.cxn.ga_{0}'.format(record)
        record = api.portal.get_registry_record(record_key)
        return record

    def get_analytics_visitors():
        f = open('privatekey.p12', 'rb')
        key = f.read()
        f.close()
        credentials = SignedJwtAssertionCredentials('xxx@developer.gserviceaccount.com',
                                                    key,
                                                    scope='https://www.googleapis.com/auth/analytics.readonly')
        http = httplib2.Http()
        http = credentials.authorize(http)
        service = build('analytics', 'v3', http=http)
        data_query = service.data().ga().get(**{
            'ids': 'ga:YOUR_PROFILE_ID_NOT_UA',
            'metrics': 'ga:visitors',
            'start_date': '2013-01-01',
            'end_date': '2015-01-01'
        })
        feed = data_query.execute()
        return feed['rows'][0][0]
