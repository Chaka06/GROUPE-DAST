from django.db import models
from django.utils.translation import gettext_lazy as _


class HeroSlide(models.Model):
    """Hero section slides — displayed as animated carousel."""
    title = models.CharField(max_length=150, verbose_name=_("Titre principal"))
    subtitle = models.CharField(max_length=250, blank=True, verbose_name=_("Sous-titre"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    cta_primary_text = models.CharField(max_length=60, default="Découvrir nos services", verbose_name=_("Bouton principal"))
    cta_primary_url = models.CharField(max_length=200, default="/services/", verbose_name=_("Lien bouton principal"))
    cta_secondary_text = models.CharField(max_length=60, blank=True, verbose_name=_("Bouton secondaire"))
    cta_secondary_url = models.CharField(max_length=200, blank=True, verbose_name=_("Lien bouton secondaire"))
    background_image = models.ImageField(upload_to="home/hero/", null=True, blank=True, verbose_name=_("Image de fond"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Ordre"))
    is_active = models.BooleanField(default=True, verbose_name=_("Actif"))

    class Meta:
        verbose_name = _("Slide hero")
        verbose_name_plural = _("Slides hero")
        ordering = ["order"]

    def __str__(self):
        return self.title


class ValueProposition(models.Model):
    """Why choose DAST cards on the homepage."""
    icon_class = models.CharField(max_length=80, default="bx bx-check-circle", verbose_name=_("Classe icône Boxicons"))
    title = models.CharField(max_length=100, verbose_name=_("Titre"))
    description = models.TextField(verbose_name=_("Description"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Ordre"))
    is_active = models.BooleanField(default=True, verbose_name=_("Actif"))

    class Meta:
        verbose_name = _("Valeur ajoutée")
        verbose_name_plural = _("Valeurs ajoutées")
        ordering = ["order"]

    def __str__(self):
        return self.title
