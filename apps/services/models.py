from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Service(models.Model):
    title = models.CharField(max_length=150, verbose_name=_("Titre du service"))
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    icon_class = models.CharField(max_length=80, default="bx bx-code-alt", verbose_name=_("Classe icône Boxicons"))
    short_description = models.CharField(max_length=250, verbose_name=_("Description courte"))
    description = models.TextField(verbose_name=_("Description détaillée"))
    cover_image = models.ImageField(upload_to="services/covers/", null=True, blank=True, verbose_name=_("Image de couverture"))
    cover_static = models.CharField(max_length=200, blank=True, default="", verbose_name=_("Image statique (chemin dans /static/)"))
    color_accent = models.CharField(max_length=7, default="#2B7FD4", verbose_name=_("Couleur accent (hex)"))
    featured = models.BooleanField(default=False, verbose_name=_("Mis en avant"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Ordre"))
    is_active = models.BooleanField(default=True, verbose_name=_("Actif"))
    meta_description = models.TextField(max_length=300, blank=True, verbose_name=_("Méta description"))

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("services:detail", kwargs={"slug": self.slug})


class ServiceFeature(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="features")
    icon_class = models.CharField(max_length=80, default="bx bx-check", verbose_name=_("Icône"))
    title = models.CharField(max_length=150, verbose_name=_("Fonctionnalité"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("Fonctionnalité")
        verbose_name_plural = _("Fonctionnalités")
        ordering = ["order"]

    def __str__(self):
        return self.title
