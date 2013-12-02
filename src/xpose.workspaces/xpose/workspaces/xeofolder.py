from five import grok
from plone import api

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


from xpose.workspaces import MessageFactory as _

XOVI_URI = 'https://api.xovi.net/index.php?'
BRAIN_URI = 'https://api.xovi.net/index.php?'


class IXeoFolder(form.Schema, IImageScaleTraversable):
    """
    Xeodash application folder
    """


class XeoFolder(Container):
    grok.implements(IXeoFolder)


class View(grok.View):
    grok.context(IXeoFolder)
    grok.require('cmf.ModifyPortalContent')
    grok.name('view')

    def available_services(self):
        keys = ('google', 'xovi', 'ac')
        data = {}
        for k in keys:
            req_key = 'xeo.cxn.{0}_api_uri'.format(k)
            api_uri = api.portal.get_registry_record(req_key)
            data[k] = api_uri
        return data


class CreateWorkspace(grok.View):
    grok.context(IXeoFolder)
    grok.require('cmf.ModifyPortalContent')
    grok.name('create-workspace')
