"""
Admin configuration for User management.
Enforces the owner-protection rules at the admin layer.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.core.exceptions import PermissionDenied
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "get_full_name", "email", "role_title", "is_owner", "is_staff", "is_active", "created_at")
    list_filter = ("is_owner", "is_staff", "is_active", "show_on_team_page")
    search_fields = ("username", "first_name", "last_name", "email")
    ordering = ("team_order", "first_name")
    readonly_fields = ("created_at", "updated_at", "last_login", "date_joined")

    fieldsets = (
        (_("Identifiants"), {"fields": ("username", "password")}),
        (_("Informations personnelles"), {
            "fields": ("first_name", "last_name", "email", "avatar", "role_title", "bio"),
        }),
        (_("Réseaux sociaux"), {
            "fields": ("linkedin_url", "twitter_url", "github_url"),
            "classes": ("collapse",),
        }),
        (_("Page équipe"), {
            "fields": ("show_on_team_page", "team_order"),
        }),
        (_("Permissions"), {
            "fields": ("is_owner", "is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            "classes": ("collapse",),
        }),
        (_("Dates"), {
            "fields": ("last_login", "date_joined", "created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "first_name", "last_name", "email", "role_title", "password1", "password2"),
        }),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Non-owners see all users; owner always has full access.
        return qs

    def has_change_permission(self, request, obj=None):
        if obj and obj.is_owner and not request.user.is_owner:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj and obj.is_owner:
            return False
        return super().has_delete_permission(request, obj)

    def get_readonly_fields(self, request, obj=None):
        readonly = list(self.readonly_fields)
        if obj and obj.is_owner:
            readonly += ["is_owner", "is_staff", "is_superuser", "is_active"]
        if not request.user.is_owner:
            readonly += ["is_owner"]
        return readonly

    def save_model(self, request, obj, form, change):
        # Prevent non-owners from granting owner status
        if not request.user.is_owner and obj.is_owner:
            raise PermissionDenied("Seul le propriétaire peut attribuer le statut de propriétaire.")
        super().save_model(request, obj, form, change)
