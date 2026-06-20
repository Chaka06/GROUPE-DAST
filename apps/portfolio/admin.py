from django.contrib import admin
from .models import Project, ProjectImage, ProjectCategory, Technology


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    ordering = ("order",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "featured", "order", "is_active", "created_at")
    list_editable = ("featured", "order", "is_active")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("technologies",)
    inlines = [ProjectImageInline]
    ordering = ("order", "-created_at")
    list_filter = ("category", "featured", "is_active")
    search_fields = ("title", "description")


@admin.register(ProjectCategory)
class ProjectCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ("name", "color")


