from django.contrib.sitemaps import Sitemap
from .models import Post, Category


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.updated_at


class CategorySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Category.objects.all()

    def lastmod(self, obj):
        latest = obj.posts.filter(status="published").order_by("-updated_at").first()
        return latest.updated_at if latest else None
