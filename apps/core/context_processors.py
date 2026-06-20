"""
Global context processors — inject site settings into every template.
"""
from django.core.cache import cache
from .models import SiteSettings


def site_settings(request):
    settings_obj = cache.get("site_settings")
    if settings_obj is None:
        settings_obj = SiteSettings.get()
        cache.set("site_settings", settings_obj, 300)
    return {"site": settings_obj}


def navigation(request):
    from apps.services.models import Service
    from apps.blog.models import Category

    nav_services = cache.get("nav_services")
    if nav_services is None:
        nav_services = list(Service.objects.filter(is_active=True).values("title", "slug", "icon_class")[:8])
        cache.set("nav_services", nav_services, 300)

    blog_categories = cache.get("blog_categories_nav")
    if blog_categories is None:
        blog_categories = list(Category.objects.all().values("name", "slug")[:6])
        cache.set("blog_categories_nav", blog_categories, 300)

    return {
        "nav_services": nav_services,
        "blog_categories": blog_categories,
    }
