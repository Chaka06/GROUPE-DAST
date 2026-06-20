from django.contrib import admin
from django.utils import timezone
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "get_subject_display", "is_read", "created_at")
    list_filter = ("is_read", "subject", "created_at")
    search_fields = ("full_name", "email", "message")
    readonly_fields = ("full_name", "email", "phone", "company", "subject", "message", "ip_address", "created_at")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    def has_add_permission(self, request):
        return False

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Marquer comme lu"

    def mark_replied(self, request, queryset):
        queryset.update(is_read=True, replied_at=timezone.now())
    mark_replied.short_description = "Marquer comme répondu"

    actions = [mark_as_read, mark_replied]
