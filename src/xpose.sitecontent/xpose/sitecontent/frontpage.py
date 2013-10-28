import random
from five import grok
from plone import api

from Acquisition import aq_inner

from plone.app.layout.navigation.interfaces import INavigationRoot
from plone.app.contentlisting.interfaces import IContentListing

from xpose.sitecontent.contentpage import IContentPage
from xpose.sitecontent.testimonial import ITestimonial


class FrontPageView(grok.View):
    grok.context(INavigationRoot)
    grok.require('cmf.ModifyPortalContent')
    grok.name('frontpage-view')

    def update(self):
        self.has_quotes = len(self.testimonials()) > 0
        if self.can_edit():
            next_url = self.home_folder().absolute_url()
            return self.request.response.redirect(next_url)

    def can_edit(self):
        return not api.user.is_anonymous()

    def home_folder(self):
        current = api.user.get_current()
        return current.getHomeFolder()

    def sections_first_row(self):
        sections = self.main_sections()
        return sections[:3]

    def sections_second_row(self):
        sections = self.main_sections()
        return sections[3:]

    def main_sections(self):
        context = aq_inner(self.context)
        catalog = api.portal.get_tool(name="portal_catalog")
        items = catalog(object_provides=IContentPage.__identifier__,
                        path=dict(query='/'.join(context.getPhysicalPath()),
                                  depth=1),
                        review_state='published',
                        sort_on='getObjPositionInParent',
                        sort_limit=6)[:6]
        results = IContentListing(items)
        return results

    def quote(self):
        quotes = self.testimonials()
        quote = random.choice(quotes)
        return quote

    def testimonials(self):
        catalog = api.portal.get_tool(name="portal_catalog")
        items = catalog(object_provides=ITestimonial.__identifier__,
                        review_state="published")
        results = IContentListing(items)
        return results
