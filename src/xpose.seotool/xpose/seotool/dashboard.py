from five import grok
from plone import api
from Acquisition import aq_inner
from plone.memoize.instance import memoize
from plone.app.layout.navigation.interfaces import INavigationRoot
from xpose.seotool.interfaces import IXposeoTool


class Dashboard(grok.View):
    grok.context(INavigationRoot)
    grok.layer(IXposeoTool)
    grok.require('zope2.View')
    grok.name('dashboard')

    def update(self):
        self.portal_url = api.portal.get().absolute_url()

    def render(self):
        if not api.user.is_anonymous():
            user = api.user.get_current()
            member_folder = user.getHomeFolder()
            home_folder = member_folder.absolute_url()
            return self.request.response.redirect(home_folder)
        else:
            return self.request.response.redirect(self.portal_url)

    @memoize
    def is_administrator(self):
        context = aq_inner(self.context)
        is_admin = False
        admin_roles = ('Site Administrator', 'Manager')
        user = api.user.get_current()
        roles = api.user.get_roles(username=user.getId(), obj=context)
        for role in roles:
            if role in admin_roles:
                is_admin = True
        return is_admin
