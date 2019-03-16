import urllib.parse
import requests
import json


class Client:

    def __init__(self, base_url):
        self.base_url = base_url

    def get(self, url):
        try:
            resp = requests.get(url)
            print(url)
            return json.loads(resp.content)
        except:
            raise


class URLHandler:

    def __init__(self, base_url):
        self.base_url = base_url

    def from_path(self, path):
        return self.base_url + path


class BaseSitemap:

    def __init__(self):
        self.client = Client(self.BASE_URL)
        self.url_handler = URLHandler(self.BASE_URL)

    def get_urls(self):
        raise NotImplementedError

    def get_url_data(self):
        raise NotImplementedError

    def get_items(self):
        items = []
        for url in self.get_urls():
            things = self.client.get(url)
            urls = self.get_url_data(things)
            if urls:
                items.extend(urls)
        return items


class XMLFileMaker:

    def __init__(self, destination):
        self.destination = destination

    def create(self, items):
        nodes = [self.make_node(k) for k in items]
        file_content = self.make_file("\n".join(nodes))
        return self.write("sitemap.xml", file_content)

    def write(self, filename, contents):
        with open(filename, 'w') as f:
            f.write(contents)
            return filename

    def make_node(self, item):
        template= """<url>\n<loc>%s/</loc>\n<lastmod>%s</lastmod>\n<changefreq>daily</changefreq>\n<priority>0.8</priority>\n</url>"""
        return template % (item.get('url'), item.get('date'))

    def make_file(self, content):
        base = """<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n%s\n</urlset>"""
        return base % content


class SitemapGenerator:

    def __init__(self, sources, target_location):
        self.source_classes = sources
        self.xml_file_maker = XMLFileMaker("/tmp")

    def create(self, many=False):
        for source_class in self.source_classes:
            items = (source_class)().get_items()
            filename = self.xml_file_maker.create(items)
            return filename
