from django.contrib import admin
from .models import HeroSlide, ValueProposition


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)


@admin.register(ValueProposition)
class ValuePropositionAdmin(admin.ModelAdmin):
    list_display = ("title", "icon_class", "order", "is_active")
    list_editable = ("order", "is_active")
    ordering = ("order",)
