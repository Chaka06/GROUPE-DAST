from django.shortcuts import render, get_object_or_404
from .models import Project, ProjectCategory


def portfolio_list(request):
    category_slug = request.GET.get("categorie")
    projects = Project.objects.filter(is_active=True).prefetch_related("technologies", "images")
    categories = ProjectCategory.objects.all()
    active_category = None

    if category_slug:
        active_category = get_object_or_404(ProjectCategory, slug=category_slug)
        projects = projects.filter(category=active_category)

    return render(request, "portfolio/list.html", {
        "projects": projects,
        "categories": categories,
        "active_category": active_category,
    })


def portfolio_detail(request, slug):
    project = get_object_or_404(Project, slug=slug, is_active=True)
    related = Project.objects.filter(is_active=True, category=project.category).exclude(pk=project.pk)[:3]
    return render(request, "portfolio/detail.html", {
        "project": project,
        "related_projects": related,
    })
