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
