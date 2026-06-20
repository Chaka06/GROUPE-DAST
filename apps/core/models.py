"""
Core site-wide models: settings, social links, partners, testimonials, FAQs.
All content is editable via the admin panel — no code changes needed.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteSettings(models.Model):
    """Singleton model for global site configuration."""

    # Identity
    site_name = models.CharField(max_length=100, default="DAST NEWGEN'SPARK", verbose_name=_("Nom du site"))
    tagline = models.CharField(max_length=200, blank=True, verbose_name=_("Slogan principal"))
    tagline_sub = models.CharField(max_length=300, blank=True, verbose_name=_("Sous-slogan"))
    about_short = models.TextField(blank=True, verbose_name=_("Description courte"))
    about_long = models.TextField(blank=True, verbose_name=_("Description complète"))
    logo = models.ImageField(upload_to="core/logo/", null=True, blank=True, verbose_name=_("Logo principal"))
    logo_white = models.ImageField(upload_to="core/logo/", null=True, blank=True, verbose_name=_("Logo blanc (footer)"))
    favicon = models.ImageField(upload_to="core/favicon/", null=True, blank=True, verbose_name=_("Favicon"))
    og_image = models.ImageField(upload_to="core/og/", null=True, blank=True, verbose_name=_("Image Open Graph"))

    # Contact
    email_main = models.EmailField(blank=True, default="dastnewgenspark@gmail.com", verbose_name=_("Email principal"))
    email_secondary = models.EmailField(blank=True, verbose_name=_("Email secondaire"))
    phone_main = models.CharField(max_length=30, blank=True, default="+225 0173176410", verbose_name=_("Téléphone principal"))
    phone_secondary = models.CharField(max_length=30, blank=True, verbose_name=_("Téléphone secondaire"))
    whatsapp = models.CharField(max_length=30, blank=True, verbose_name=_("Numéro WhatsApp"))
    address = models.TextField(blank=True, verbose_name=_("Adresse physique"))
    google_maps_url = models.URLField(blank=True, verbose_name=_("Lien Google Maps"))
    google_maps_embed = models.TextField(blank=True, verbose_name=_("Code d'intégration Google Maps"))

    # Social
    facebook_url = models.URLField(blank=True, verbose_name=_("Facebook"))
    instagram_url = models.URLField(blank=True, verbose_name=_("Instagram"))
    linkedin_url = models.URLField(blank=True, verbose_name=_("LinkedIn"))
    tiktok_url = models.URLField(blank=True, verbose_name=_("TikTok"))
    youtube_url = models.URLField(blank=True, verbose_name=_("YouTube"))
    twitter_url = models.URLField(blank=True, verbose_name=_("Twitter / X"))
    github_url = models.URLField(blank=True, verbose_name=_("GitHub"))

    # SEO
    meta_description = models.TextField(max_length=300, blank=True, verbose_name=_("Méta description"))
    meta_keywords = models.TextField(blank=True, verbose_name=_("Mots-clés SEO"))
    google_analytics_id = models.CharField(max_length=50, blank=True, verbose_name=_("ID Google Analytics"))
    google_tag_manager_id = models.CharField(max_length=50, blank=True, verbose_name=_("ID Google Tag Manager"))

    # Stats (displayed on homepage)
    stat_projects = models.PositiveIntegerField(default=0, verbose_name=_("Projets réalisés"))
    stat_clients = models.PositiveIntegerField(default=0, verbose_name=_("Clients satisfaits"))
    stat_years = models.PositiveIntegerField(default=0, verbose_name=_("Années d'expérience"))
    stat_team = models.PositiveIntegerField(default=0, verbose_name=_("Membres de l'équipe"))

    class Meta:
        verbose_name = _("Paramètres du site")
        verbose_name_plural = _("Paramètres du site")

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1  # Enforce singleton
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Partner(models.Model):
    name = models.CharField(max_length=150, verbose_name=_("Nom du partenaire"))
    logo = models.ImageField(upload_to="core/partners/", verbose_name=_("Logo"))
    website_url = models.URLField(blank=True, verbose_name=_("Site web"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Ordre"))
    is_active = models.BooleanField(default=True, verbose_name=_("Actif"))

    class Meta:
        verbose_name = _("Partenaire")
        verbose_name_plural = _("Partenaires")
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    client_name = models.CharField(max_length=150, verbose_name=_("Nom du client"))
    client_role = models.CharField(max_length=150, blank=True, verbose_name=_("Poste / Entreprise"))
    client_photo = models.ImageField(upload_to="core/testimonials/", null=True, blank=True, verbose_name=_("Photo"))
    content = models.TextField(verbose_name=_("Témoignage"))
    rating = models.PositiveSmallIntegerField(default=5, choices=[(i, i) for i in range(1, 6)], verbose_name=_("Note"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Ordre"))
    is_active = models.BooleanField(default=True, verbose_name=_("Actif"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Témoignage")
        verbose_name_plural = _("Témoignages")
        ordering = ["order", "-created_at"]

    def __str__(self):
        return f"{self.client_name} — {self.rating}/5"


class FAQ(models.Model):
    question = models.CharField(max_length=300, verbose_name=_("Question"))
    answer = models.TextField(verbose_name=_("Réponse"))
    category = models.CharField(max_length=100, blank=True, verbose_name=_("Catégorie"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Ordre"))
    is_active = models.BooleanField(default=True, verbose_name=_("Actif"))

    class Meta:
        verbose_name = _("FAQ")
        verbose_name_plural = _("FAQ")
        ordering = ["order"]

    def __str__(self):
        return self.question
