"""
Custom User model for DAST NEWGEN'SPARK.

Hierarchy:
  - owner (is_owner=True): unique super-admin. Cannot be demoted or deleted by anyone else.
  - admin (is_staff=True, is_superuser=True): secondary admin created by owner.
  - staff (is_staff=True): content managers.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Extended user with owner flag and profile fields."""

    is_owner = models.BooleanField(
        default=False,
        verbose_name=_("Propriétaire principal"),
        help_text=_("Seul le propriétaire peut créer/gérer les administrateurs secondaires."),
    )
    avatar = models.ImageField(
        upload_to="accounts/avatars/",
        null=True,
        blank=True,
        verbose_name=_("Photo de profil"),
    )
    role_title = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_("Titre / Poste"),
    )
    bio = models.TextField(blank=True, verbose_name=_("Biographie"))
    linkedin_url = models.URLField(blank=True, verbose_name=_("LinkedIn"))
    twitter_url = models.URLField(blank=True, verbose_name=_("Twitter / X"))
    github_url = models.URLField(blank=True, verbose_name=_("GitHub"))
    show_on_team_page = models.BooleanField(
        default=False,
        verbose_name=_("Afficher sur la page équipe"),
    )
    team_order = models.PositiveIntegerField(default=0, verbose_name=_("Ordre d'affichage"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Créé le"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Modifié le"))

    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")
        ordering = ["team_order", "first_name"]

    def __str__(self):
        return self.get_full_name() or self.username

    @property
    def display_name(self):
        return self.get_full_name() or self.username

    def delete(self, *args, **kwargs):
        """The owner account can never be deleted programmatically."""
        if self.is_owner:
            raise PermissionError("Le compte du propriétaire principal ne peut pas être supprimé.")
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        """Ensure only one owner exists and owner always keeps staff/superuser status."""
        if self.is_owner:
            self.is_staff = True
            self.is_superuser = True
        super().save(*args, **kwargs)
