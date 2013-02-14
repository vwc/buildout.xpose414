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
