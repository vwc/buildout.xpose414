import json
from Acquisition import aq_inner
from five import grok
from plone import api
from zope.component import getUtility

from z3c.form import group, field
from zope import schema
from zope.lifecycleevent import modified
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

    def render(self):
        context = aq_inner(self.context)
        next_url = context.absolute_url()
        self._build_report()
        return self.request.response.redirect(next_url)

    def _build_report(self):
        context = aq_inner(self.context)
        report = {}
        stored_report = getattr(context, 'report_xovi', None)
        if stored_report:
            report = json.loads(stored_report)
        tool = getUtility(IXoviTool)
        status = tool.status()
        if status['status'] == '0k.':
            ses = tool.get(
                service=u'seo',
                method=u'getSearchEngines',
            )
            report['getSearchengines'] = ses
            kws = tool.get(
                service=u'seo',
                method=u'getKeywords',
                sengine=u'google.de',
                domain=u'xpose414.de',
            )
            report['getKeywords'] = kws
            daily_kws = tool.get(
                service=u'seo',
                method=u'getDailyKeywords',
            )
            report['getDailyKeywords'] = daily_kws
            lost_kws = tool.get(
                service=u'seo',
                method=u'getLostKeywords',
                sengineid=u'1',
                domain=u'xpose414.de',
            )
            report['getLostKeywords'] = lost_kws
        data = json.dumps(report)
        setattr(context, 'report_xovi', data)
        modified(context)
        context.reindexObject(idxs='modified')
        return report
