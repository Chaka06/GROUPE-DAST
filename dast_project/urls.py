"""DAST NEWGEN'SPARK — Root URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

from apps.blog.sitemaps import PostSitemap, CategorySitemap
from apps.portfolio.sitemaps import ProjectSitemap
from apps.core.sitemaps import StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
    "posts": PostSitemap,
    "categories": CategorySitemap,
    "projects": ProjectSitemap,
}

urlpatterns = [
    # ── Admin (accessible uniquement via /dast/) ──────────────────────────
    path("dast/", admin.site.urls),

    # ── Public ────────────────────────────────────────────────────────────
    path("", include("apps.home.urls")),
    path("services/", include("apps.services.urls")),
    path("portfolio/", include("apps.portfolio.urls")),
    path("blog/", include("apps.blog.urls")),
    path("contact/", include("apps.contact.urls")),
    path("equipe/", include("apps.accounts.urls")),

    # ── SEO ───────────────────────────────────────────────────────────────
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),

    # ── Summernote ────────────────────────────────────────────────────────
    path("summernote/", include("django_summernote.urls")),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path("__debug__/", include(debug_toolbar.urls)),
    ] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
