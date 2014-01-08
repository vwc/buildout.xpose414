from Acquisition import aq_inner
from Acquisition import aq_parent
from five import grok
from zope import schema
from zope.schema import getFieldsInOrder
from zope.component import getUtility

from zope.lifecycleevent import modified

from plone.directives import form
from z3c.form import button

from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from plone.dexterity.interfaces import IDexterityFTI
from Products.statusmessages.interfaces import IStatusMessage

from xpose.seotool.seotool import ISeoTool

from xpose.seotool import MessageFactory as _

usergroups = SimpleVocabulary([
    SimpleTerm(value=u'staff', title=_(u'Xpose414 Staff')),
    SimpleTerm(value=u'customers', title=_(u'Customers'))
])


class IUserCreation(form.Schema):

    fullname = schema.TextLine(
        title=_(u"Banner Headline"),
        required=False,
    )
    email = schema.TextLine(
        title=_(u"E-Mail"),
        description=_(u"Enter a valid E-Mail address. Note: this address will "
                      u"act as the login name"),
        required=True,
    )
    organizer = schema.Choice(
        title=_(u"Organiser"),
        source=usergroups,
        required=True,
        default=u'customers',
    )


class UserCreationForm(form.SchemaEditForm):
    grok.context(ISeoTool)
    grok.require('cmf.AddPortalContent')
    grok.name('edit-banner')

    schema = IUserCreation
    ignoreContext = False
    css_class = 'app-form'

    label = _(u"Edit content panel")

    def updateActions(self):
        super(UserCreationForm, self).updateActions()
        self.actions['save'].addClass("btn btn-primary btn-editpanel")
        self.actions['cancel'].addClass("btn btn-default")

    @button.buttonAndHandler(_(u"Save"), name="save")
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)

    @button.buttonAndHandler(_(u"cancel"))
    def handleCancel(self, action):
        context = aq_inner(self.context)
        IStatusMessage(self.request).addStatusMessage(
            _(u"Content block factory has been cancelled."),
            type='info')
        return self.request.response.redirect(context.absolute_url())

    def getContent(self):
        context = aq_inner(self.context)
        fti = getUtility(IDexterityFTI,
                         name='atix.sitecontent.contentbanner')
        schema = fti.lookupSchema()
        fields = getFieldsInOrder(schema)
        data = {}
        for key, value in fields:
            data[key] = getattr(context, key, value)
        return data

    def applyChanges(self, data):
        context = aq_inner(self.context)
        fti = getUtility(IDexterityFTI,
                         name='atix.sitecontent.contentbanner')
        schema = fti.lookupSchema()
        fields = getFieldsInOrder(schema)
        for key, value in fields:
            try:
                new_value = data[key]
                setattr(context, key, new_value)
            except KeyError:
                continue
        modified(context)
        context.reindexObject(idxs='modified')
        IStatusMessage(self.request).addStatusMessage(
            _(u"The banner has successfully been updated"),
            type='info')
        next_url = context.absolute_url()
        parent = aq_parent(context)
        next_url = parent.absolute_url()
        return self.request.response.redirect(next_url)
