from django.contrib.sitemaps import Sitemap
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = "weekly"

    def items(self):
        return ["home:index", "services:list", "portfolio:list", "blog:list", "contact:index", "accounts:team"]

    def location(self, item):
        return reverse(item)
