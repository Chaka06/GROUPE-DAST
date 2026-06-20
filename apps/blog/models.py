"""
Blog models: Category, Tag, Post.
Posts track their author (auto-assigned to the logged-in user on save).
"""
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Nom"))
    slug = models.SlugField(max_length=110, unique=True, blank=True)
    description = models.TextField(blank=True, verbose_name=_("Description"))
    cover_image = models.ImageField(upload_to="blog/categories/", null=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("Catégorie")
        verbose_name_plural = _("Catégories")
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:category", kwargs={"slug": self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=80, verbose_name=_("Tag"))
    slug = models.SlugField(max_length=90, unique=True, blank=True)

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(
            status=Post.Status.PUBLISHED,
            published_at__lte=timezone.now(),
        )


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", _("Brouillon")
        PUBLISHED = "published", _("Publié")
        SCHEDULED = "scheduled", _("Programmé")

    title = models.CharField(max_length=250, verbose_name=_("Titre"))
    slug = models.SlugField(max_length=270, unique=True, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="posts",
        verbose_name=_("Auteur"),
        editable=False,  # Set programmatically, not by the form user
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="posts", verbose_name=_("Catégorie"),
    )
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=_("Tags"))
    cover_image = models.ImageField(upload_to="blog/covers/", null=True, blank=True, verbose_name=_("Image de couverture"))
    excerpt = models.TextField(max_length=400, blank=True, verbose_name=_("Extrait"))
    content = models.TextField(verbose_name=_("Contenu"))
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT, verbose_name=_("Statut"),
    )
    featured = models.BooleanField(default=False, verbose_name=_("Article vedette"))
    published_at = models.DateTimeField(null=True, blank=True, verbose_name=_("Date de publication"))
    meta_description = models.TextField(max_length=300, blank=True, verbose_name=_("Méta description"))
    views_count = models.PositiveIntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")
        ordering = ["-published_at", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})

    @property
    def reading_time(self):
        word_count = len(self.content.split())
        minutes = max(1, round(word_count / 200))
        return minutes

    def increment_views(self):
        Post.objects.filter(pk=self.pk).update(views_count=models.F("views_count") + 1)
