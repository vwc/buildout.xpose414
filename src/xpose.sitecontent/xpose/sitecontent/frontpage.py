from five import grok
from plone import api

from plone.app.layout.navigation.interfaces import INavigationRoot

from xpose.sitecontent.testimonial import ITestimonial


class FrontPageView(grok.View):
    grok.context(INavigationRoot)
    grok.require('zope2.View')
    grok.name('frontpage-view')

    def testimonials(self):
        catalog = api.portal.get_tool(name="portal_catalog")
        items = catalog(object_provides=ITestimonial.__identifier__,
                        review_state="published")
        return items
