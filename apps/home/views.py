from django.shortcuts import render
from django.views.generic import TemplateView

from apps.core.models import Partner, Testimonial, FAQ
from apps.services.models import Service
from apps.portfolio.models import Project
from apps.blog.models import Post
from .models import HeroSlide, ValueProposition


class HomeView(TemplateView):
    template_name = "home/index.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["hero_slides"] = HeroSlide.objects.filter(is_active=True)
        ctx["values"] = ValueProposition.objects.filter(is_active=True)
        ctx["services"] = Service.objects.filter(is_active=True, featured=True)[:6]
        ctx["projects"] = Project.objects.filter(is_active=True, featured=True)[:6]
        ctx["posts"] = Post.published.order_by("-published_at")[:3]
        ctx["testimonials"] = Testimonial.objects.filter(is_active=True)
        ctx["partners"] = Partner.objects.filter(is_active=True)
        ctx["faqs"] = FAQ.objects.filter(is_active=True)[:8]
        return ctx
