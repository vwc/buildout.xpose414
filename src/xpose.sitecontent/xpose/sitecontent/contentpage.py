from Acquisition import aq_inner
from five import grok
from zope import schema
from plone import api

from plone.directives import dexterity, form

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage

from plone.app.textfield import RichText

from xpose.sitecontent import MessageFactory as _


class IContentPage(form.Schema, IImageScaleTraversable):
    """
    Folderish content page
    """
    text = RichText(
        title=_(u"Body Text"),
        required=True,
    )
    image = NamedBlobImage(
        title=_(u"Preview Image"),
        description=_(u"Upload optional preview image that can be used in "
                      u"listings and search results"),
        required=False,
    )
    caption = schema.TextLine(
        title=_(u"Preview Image Caption"),
        required=False,
    )


class ContentPage(dexterity.Container):
    grok.implements(IContentPage)


class View(grok.View):
    grok.context(IContentPage)
    grok.require('zope2.View')
    grok.name('view')

    def update(self):
        self.has_subpages = len(self.subpages()) > 0
        if self.has_single_subpage():
            redirect_url = self.redirect_to_subpage()
            self.request.response.redirect(redirect_url)

    def has_single_subpage(self):
        return len(self.subpages()) == 1

    def redirect_to_subpage(self):
        pages = self.subpages()
        page = pages[0]
        target_url = page.getURL()
        return target_url

    def subpages(self):
        context = aq_inner(self.context)
        items = context.restrictedTraverse('@@folderListing')(
            portal_type='xpose.sitecontent.contentpage',
            review_state='published')
        return items
