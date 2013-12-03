from Acquisition import aq_inner
from five import grok
from plone import api
from zope.interface import Interface
from plone.memoize.instance import memoize

from plone.app.layout.viewlets.interfaces import IPortalFooter
from plone.app.contentlisting.interfaces import IContentListing


class SidebarViewlet(grok.Viewlet):
    grok.context(Interface)
    grok.viewletmanager(IPortalFooter)
    grok.require('zope2.View')
    grok.name('xpose.seotool.SidebarViewlet')

    def update(self):
        self.portal_url = api.portal.get().absolute_url()

    @memoize
    def user_displayname(self):
        """Get the username of the currently logged in user
        """
        if api.user.is_anonymous():
            return None
        member = api.user.get_current()
        userid = member.getId()
        fullname = userid
        fullname = member.getProperty('fullname') or fullname
        return fullname

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
