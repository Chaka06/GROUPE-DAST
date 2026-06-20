from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Technology(models.Model):
    name = models.CharField(max_length=80, verbose_name=_("Technologie"))
    icon_class = models.CharField(max_length=80, blank=True, verbose_name=_("Classe icône"))
    color = models.CharField(max_length=7, default="#2B7FD4", verbose_name=_("Couleur badge"))

    class Meta:
        verbose_name = _("Technologie")
        verbose_name_plural = _("Technologies")
        ordering = ["name"]

    def __str__(self):
        return self.name


class ProjectCategory(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Catégorie"))
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = _("Catégorie de projet")
        verbose_name_plural = _("Catégories de projets")
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name=_("Titre du projet"))
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.ForeignKey(
        ProjectCategory, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="projects", verbose_name=_("Catégorie"),
    )
    technologies = models.ManyToManyField(Technology, blank=True, verbose_name=_("Technologies"))
    short_description = models.CharField(max_length=280, verbose_name=_("Description courte"))
    description = models.TextField(verbose_name=_("Description détaillée"))
    cover_image = models.ImageField(upload_to="portfolio/covers/", verbose_name=_("Image principale"))
    client_name = models.CharField(max_length=150, blank=True, verbose_name=_("Nom du client"))
    project_url = models.URLField(blank=True, verbose_name=_("Lien vers le projet"))
    github_url = models.URLField(blank=True, verbose_name=_("Lien GitHub"))
    featured = models.BooleanField(default=False, verbose_name=_("Mis en avant"))
    order = models.PositiveIntegerField(default=0, verbose_name=_("Ordre"))
    is_active = models.BooleanField(default=True, verbose_name=_("Actif"))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Projet")
        verbose_name_plural = _("Projets")
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("portfolio:detail", kwargs={"slug": self.slug})


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="portfolio/gallery/", verbose_name=_("Image"))
    caption = models.CharField(max_length=200, blank=True, verbose_name=_("Légende"))
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("Image du projet")
        verbose_name_plural = _("Images du projet")
        ordering = ["order"]

    def __str__(self):
        return f"Image — {self.project.title}"
