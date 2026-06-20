from django.db import models
from django.utils.translation import gettext_lazy as _


class ContactMessage(models.Model):
    class Subject(models.TextChoices):
        WEB = "web", _("Développement web")
        MARKETING = "marketing", _("Marketing digital")
        COMMUNICATION = "communication", _("Communication")
        DIGITAL = "digital", _("Services numériques")
        PARTNERSHIP = "partnership", _("Partenariat")
        OTHER = "other", _("Autre")

    full_name = models.CharField(max_length=200, verbose_name=_("Nom complet"))
    email = models.EmailField(verbose_name=_("Email"))
    phone = models.CharField(max_length=30, blank=True, verbose_name=_("Téléphone"))
    company = models.CharField(max_length=150, blank=True, verbose_name=_("Entreprise"))
    subject = models.CharField(max_length=30, choices=Subject.choices, default=Subject.OTHER, verbose_name=_("Sujet"))
    message = models.TextField(verbose_name=_("Message"))
    is_read = models.BooleanField(default=False, verbose_name=_("Lu"))
    replied_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Répondu le"))
    ip_address = models.GenericIPAddressField(null=True, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Reçu le"))

    class Meta:
        verbose_name = _("Message de contact")
        verbose_name_plural = _("Messages de contact")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} — {self.get_subject_display()}"
