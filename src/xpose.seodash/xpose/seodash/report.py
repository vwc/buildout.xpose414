from Acquisition import aq_inner
from five import grok
from plone import api
from zope.component import getUtility

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from plone.dexterity.content import Container

from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile
from plone.namedfile.interfaces import IImageScaleTraversable

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from xpose.seotool.xovi import report_methods
from xpose.seotool.xovi import IXoviTool

from xpose.seodash import MessageFactory as _


# Interface class; used to define content-type schema.

class IReport(form.Schema, IImageScaleTraversable):
    """
    A collection of metrics and dimensions
    """
    site = schema.URI(
        title=_(u"Site URI"),
        required=True,
    )
    report_xovi = schema.TextLine(
        title=_(u"Xovi Report"),
        description=_(u"Automatically updated report consisting of predefined "
                      u"methods and values"),
        required=False,
    )


class Report(Container):
    grok.implements(IReport)

    # Add your class methods and properties here
    pass


class View(grok.View):
    grok.context(IReport)
    grok.require('zope2.View')
    grok.name('view')


class RequestReport(grok.View):
    grok.context(IReport)
    grok.require('cmf.ManagePortal')
    grok.name('build-report')

    def _build_report(self):
        report = {}
        tool = getUtility(IXoviTool)
        status = tool.status()
        if status == '0k.':
            for method in report_methods:
                data = tool.get(method=method)
                report['method'] = data
        return report
