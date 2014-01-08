from five import grok
from plone import api

from zope.schema.vocabulary import SimpleVocabulary

from zope.schema.interfaces import IContextSourceBinder
from xpose.seotool.seotool import ISeoTool


class UserManager(grok.View):
    grok.context(ISeoTool)
    grok.require('cmf.ManagePortal')
    grok.name('manage-users')

    def update(self):
        self.has_users = len(self.customers()) > 0

    def customers(self):
        return api.user.get_users(groupname='customers')


class GroupMembers(object):
    """ Context source binder to provide a vocabulary of users in a given
        group.
    """
    grok.implements(IContextSourceBinder)

    def __init__(self, group_name):
        self.group_name = group_name

    def __call__(self, context):
        group = api.group.get(groupname=self.group_name)
        terms = []
        if group is not None:
            for member_id in api.user.get_users(groupname=group):
                user = api.user.get(username=member_id)
                if user is not None:
                    member_name = user.getProperty('fullname') or member_id
                    terms.append(SimpleVocabulary.createTerm(
                        member_id, str(member_id), member_name)
                    )

        return SimpleVocabulary(terms)
