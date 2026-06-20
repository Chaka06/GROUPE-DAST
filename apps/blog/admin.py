from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Category, Tag, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ("name", "order")
    list_editable = ("order",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ("content",)
    list_display = ("title", "author", "category", "status", "featured", "published_at", "views_count")
    list_filter = ("status", "featured", "category")
    list_editable = ("status", "featured")
    search_fields = ("title", "excerpt", "content")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    readonly_fields = ("views_count", "created_at", "updated_at", "author_display")
    date_hierarchy = "published_at"

    fieldsets = (
        ("Contenu", {"fields": ("title", "slug", "cover_image", "excerpt", "content")}),
        ("Classification", {"fields": ("category", "tags")}),
        ("Publication", {"fields": ("status", "published_at", "featured")}),
        ("SEO", {"fields": ("meta_description",), "classes": ("collapse",)}),
        ("Métadonnées", {"fields": ("author_display", "views_count", "created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def author_display(self, obj):
        return str(obj.author) if obj.author else "—"
    author_display.short_description = "Auteur"

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)
