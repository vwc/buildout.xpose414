import json
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
from plone.dexterity.content import Container
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable


from xpose.seotool import MessageFactory as _


class ISeoTool(form.Schema, IImageScaleTraversable):
    """
    Seo Application utility tool
    """


class SeoTool(Container):
    grok.implements(ISeoTool)


class View(grok.View):
    grok.context(ISeoTool)
    grok.require('zope2.View')
    grok.name('view')

    def available_services(self):
        services = {
            u'google': _(u"Google Analytics"),
            u'xovi': _(u"XOVI"),
            u'ac': _(u"activeCollab"),
        }
        data = []
        for s in services:
            item = {}
            req_key = 'xeo.cxn.{0}_api_uri'.format(s)
            api_uri = api.portal.get_registry_record(req_key)
            item['name'] = services[s]
            item['sid'] = s
            item['uri'] = api_uri
            data.append(item)
        return data

    def service_status(self, service):
        url = service['uri']
        name = service['sid']
        if name == 'ac':
            url = url + '?check_if_alive=1&format=json"'
        if name == 'xovi':
            data = {
                'key': u'myPersonalKey',
                'service': u'user',
                'method':  u'getCreditState',
                'format':  u'json',
            }
            url = url + '?' + urlencode(data)
        try:
            st = self._check_service_status(url)
        except HTTPError:
            msg = 'Not available'
        if st:
            msg = service['name'] + st
        return msg

    def get_state_klass(self, statuscode):
        state = {'statuscode': 'available',
                 'klass': 'text-success'}
        if statuscode == 'Not available':
            state = {'statuscode': 'not available',
                     'klass': 'text-danger'}
        return state

    def _check_service_status(self, service_url):
        with contextlib.closing(urlopen(service_url)) as response:
            return response.read().decode('utf-8')


class SetupAnalytics(grok.View):
    grok.context(ISeoTool)
    grok.require('zope2.View')
    grok.name('setup-google')

    def get_metrics(self):
        url = 'https://www.googleapis.com/analytics/v3/metadata/ga/columns?pp=1'
        with contextlib.closing(urlopen(url)) as response:
            resp = response.read().decode('utf-8')
            data = json.loads(resp)
            return data

    def get_stateklass(self, code):
        klass = 'text-success'
        if code == 'DEPRECATED':
            klass = 'text-danger'
        return klass


class SetupXovi(grok.View):
    grok.context(ISeoTool)
    grok.require('zope2.View')
    grok.name('setup-xovi')


class SetupAC(grok.View):
    grok.context(ISeoTool)
    grok.require('zope2.View')
    grok.name('setup-ac')
