from sitemap.sitemap import BaseSitemap


class JobSitemap(BaseSitemap):

    BASE_URL = "http://localhost:4000/api"

    def get_urls(self):
        return [self.url_handler.from_path("/jobs")]

    def get_url_data(self, resp):
        return [self.serialize(k) for k in resp]

    def serialize(self, item):
        return {
            "url": self.url_handler.from_path("/jobs/%s" % item["slug"]),
            "date": None
        }
