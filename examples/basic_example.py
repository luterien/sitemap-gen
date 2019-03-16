#!/usr/bin/env python
from sitemap.sitemap import BaseSitemap, SitemapGenerator


class JobSitemap(BaseSitemap):

    BASE_URL = "http://localhost:4000/api"

    def get_urls(self):
        return [self.url_handler.from_path("/jobs")]

    def get_url_data(self, resp):
        return [self.serialize(k) for k in resp]

    def serialize(self, item):
        return {
            "url": self.url_handler.from_path("/jobs/%s" % item["slug"]),
            "date": "YYYY-MM-DD"
        }


sitemap_sources = [JobSitemap,]
sitemap_generator = SitemapGenerator(
    sources=sitemap_sources,
    target_location="/tmp"
)
filename = sitemap_generator.create()
