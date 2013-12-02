from five import grok

from zope.interface import Interface


class ISeoTool(Interface):
    """ Api call processing and session data storage """


class SeoTool(grok.GlobalUtility):
    grok.provides(ISeoTool)
