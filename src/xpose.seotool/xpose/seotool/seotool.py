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

from Acquisition import aq_inner
from AccessControl import Unauthorized
from five import grok
from plone import api
from zope.component import getUtility
from zope.component import getMultiAdapter
from plone.dexterity.content import Container
from plone.directives import form
from plone.namedfile.interfaces import IImageScaleTraversable
from Products.CMFPlone.utils import safe_unicode

from xpose.seotool.xovi import IXoviTool

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
        status = 'OK'
        info = {}
        if name == 'ac':
            info['name'] = name
            api_token = '24-jDsvH7s8fv3BGt3sx0bESliMXYjRhsjzORv8NA89'
            token = '&auth_api_token={0}'.format(api_token)
            # url = url + '?check_if_alive=1&format=json' + token
            url = url + '?path_info=info&format=json' + token
            try:
                status = self._check_service_status(url)
            except HTTPError:
                status = 'Not available'
            import pdb; pdb.set_trace( )
            info['status'] = status
            info['response'] = status
        if name == 'xovi':
            info['name'] = name
            xovi_tool = getUtility(IXoviTool)
            xovi_status = xovi_tool.status()
            state_info = json.loads(xovi_status)
            info['status'] = state_info['apiErrorMessage']
            info['response'] = state_info['apiResult']
        status = info
        return status

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


class AddAuthToken(grok.View):
    grok.context(ISeoTool)
    grok.require('zope2.View')
    grok.name('add-auth-token')

    def update(self):
        context = aq_inner(self.context)
        self.errors = {}
        unwanted = ('_authenticator', 'form.button.Submit')
        required = ('service')
        if 'form.button.Submit' in self.request:
            authenticator = getMultiAdapter((context, self.request),
                                            name=u"authenticator")
            if not authenticator.verify():
                raise Unauthorized
            form = self.request.form
            form_data = {}
            form_errors = {}
            errorIdx = 0
            for value in form:
                if value not in unwanted:
                    form_data[value] = safe_unicode(form[value])
                    if not form[value] and value in required:
                        error = {}
                        error['active'] = True
                        error['msg'] = _(u"This field is required")
                        form_errors[value] = error
                        errorIdx += 1
                    else:
                        error = {}
                        error['active'] = False
                        error['msg'] = form[value]
                        form_errors[value] = error
            if errorIdx > 0:
                self.errors = form_errors
            else:
                self._set_auth_token(form)

    def _set_auth_token(self, data):
        service = data['service']
        if service == 'google':
            client_id = data['client_id']
            client_secret = data['client_secret']
            record_id = 'xeo.cxn.{0}_client_id'.format(service)
            record_secret = 'xeo.cxn.{0}_client_secret'.format(service)
            api.portal.set_registry_record(record_id, client_id)
            api.portal.set_registry_record(record_secret, client_secret)
        else:
            token = data['token']
            record = 'xeo.cxn.{0}_client_key'.format(service)
            api.portal.set_registry_record(record, token)
        portal_url = api.portal.get().absolute_url()
        param = '/adm/@@setup-{0}'.format(service)
        url = portal_url + param
        return self.request.response.redirect(url)


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

    def update(self):
        self.errors = {}

    def default_value(self, error):
        value = ''
        if error['active'] is False:
            value = error['msg']
        return value
