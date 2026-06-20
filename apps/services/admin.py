from django.contrib import admin
from .models import Service, ServiceFeature


class ServiceFeatureInline(admin.TabularInline):
    model = ServiceFeature
    extra = 1
    ordering = ("order",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "featured", "order", "is_active")
    list_editable = ("featured", "order", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ServiceFeatureInline]
    ordering = ("order",)
