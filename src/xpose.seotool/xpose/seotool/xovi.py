from five import grok
from plone import api
from zope.interface import Interface


SERVICE_URI = 'https://api.xovi.net/index.php?'


class IXoviTool(Interface):
    """ Api call processing and session data storage """


class XoviTool(grok.GlobalUtility):
    grok.provides(IXoviTool)
