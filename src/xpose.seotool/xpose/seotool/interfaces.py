from zope import schema
from zope.interface import Interface

from xpose.seotool import MessageFactory as _


class ISeoToolContent(Interface):
    """A general Interface to mark all press content """


class IXposeoTool(Interface):
    """ A marker inteface for a specific theme layer """


class IXeoSettings(Interface):
    """ API secrets, tokens and keys stored in the registry """

    google_api_uri = schema.TextLine(
        title=_(u"Google API URI"),
        default=u"https://www.googleapis.com/auth/analytics.readonly"
    )
    google_auth_uri = schema.TextLine(
        title=_(u"Google Auth URI"),
        default=u"https://accounts.google.com/o/oauth2/auth"
    )
    google_token_uri = schema.TextLine(
        title=_(u"Google Token URI"),
        default=u"https://accounts.google.com/o/oauth2/token"
    )
    google_client_id = schema.TextLine(
        title=_(u"Google Client ID")
    )
    google_client_secret = schema.TextLine(
        title=_(u"Google Client Secret")
    )
    xovi_api_uri = schema.TextLine(
        title=_(u"Xovi API URI"),
        default=u"https://api.xovi.net/index.php"
    )
    xovi_client_key = schema.TextLine(
        title=_(u"Xovi Client Key"),
    )
    ac_api_uri = schema.TextLine(
        title=_(u"ActiveCollab API URI"),
        default=u"http://brain.xpose414.de/api.php"
    )
    ac_client_key = schema.TextLine(
        title=_(u"ActiveCollab Client Key"),
    )
