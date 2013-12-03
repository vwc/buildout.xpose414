from Acquisition import aq_inner
from five import grok
from plone import api

from plone.memoize.instance import memoize
from plone.app.layout.navigation.interfaces import INavigationRoot


class FrontPageView(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('frontpage-router')

    def update(self):
        self.next_url = self.redirection_target()

    def render(self):
        return self.request.response.redirect(self.next_url)

    def redirection_target(self):
        portal_url = api.portal.get().absolute_url()
        if api.user.is_anonymous():
            url = portal_url * '/login'
        else:
            if self.is_administrator():
                url = portal_url + '/adm'
            else:
                url = self.user_homeurl()
        return url

    @memoize
    def user_homeurl(self):
        member = api.user.get_current()
        userid = member.getId()
        return "%s/workspace/%s" % (api.portal.get().absolute_url(),
                                    userid)

    def is_administrator(self):
        context = aq_inner(self.context)
        is_adm = False
        if not api.user.is_anonymous():
            user = api.user.get_current()
            roles = api.user.get_roles(username=user.getId(), obj=context)
            if 'Manager' or 'Site Administrator' in roles:
                is_adm = True
        return is_adm
