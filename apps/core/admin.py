from django.contrib import admin
from django.core.cache import cache
from .models import SiteSettings, Partner, Testimonial, FAQ


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Identité", {
            "fields": ("site_name", "tagline", "tagline_sub", "about_short", "about_long",
                       "logo", "logo_white", "favicon", "og_image"),
        }),
        ("Contact", {
            "fields": ("email_main", "email_secondary", "phone_main", "phone_secondary",
                       "whatsapp", "address", "google_maps_url", "google_maps_embed"),
        }),
        ("Réseaux sociaux", {
            "fields": ("facebook_url", "instagram_url", "linkedin_url", "tiktok_url",
                       "youtube_url", "twitter_url", "github_url"),
        }),
        ("Statistiques", {
            "fields": ("stat_projects", "stat_clients", "stat_years", "stat_team"),
        }),
        ("SEO", {
            "fields": ("meta_description", "meta_keywords", "google_analytics_id", "google_tag_manager_id"),
            "classes": ("collapse",),
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        cache.delete("site_settings")


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("client_name", "client_role", "rating", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "category", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("category",)
    ordering = ("order",)
