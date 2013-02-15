from five import grok
from plone.directives import dexterity, form

from zope import schema

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedBlobImage


from xpose.sitecontent import MessageFactory as _


class ITestimonial(form.Schema, IImageScaleTraversable):
    """
    A customer quote
    """
    title = schema.TextLine(
        title=_(u"Title"),
        required=True,
    )
    customer = schema.TextLine(
        title=_("Customer"),
        required=True,
    )
    position = schema.TextLine(
        title=_(u"Position in Company"),
        description=_(u"Optional position like CEO"),
        required=False,
    )
    company = schema.TextLine(
        title=_(u"Company Name"),
        required=True,
    )
    statement = schema.Text(
        title=_(u"Statement"),
        description=_(u"Enter customer statement"),
        required=True,
    )
    logo = NamedBlobImage(
        title=_(u"Company Logo"),
        description=_(u"Upload optional company logo. Since this image file "
                      u"will only be displayed in a scaled down version the "
                      u"uploaded file should be small"),
        required=False,
    )


class Testimonial(dexterity.Item):
    grok.implements(ITestimonial)


class View(grok.View):
    grok.context(ITestimonial)
    grok.require('zope2.View')
    grok.name('view')
