from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Category, Tag


def post_list(request):
    posts = Post.published.select_related("author", "category").prefetch_related("tags")
    category_slug = request.GET.get("categorie")
    tag_slug = request.GET.get("tag")
    query = request.GET.get("q", "").strip()
    active_category = None
    active_tag = None

    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=active_category)

    if tag_slug:
        active_tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags=active_tag)

    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(excerpt__icontains=query) | Q(content__icontains=query))

    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "blog/list.html", {
        "page_obj": page_obj,
        "categories": Category.objects.all(),
        "active_category": active_category,
        "active_tag": active_tag,
        "query": query,
        "featured_posts": Post.published.filter(featured=True)[:3],
    })


def post_detail(request, slug):
    post = get_object_or_404(Post.published, slug=slug)
    post.increment_views()
    related = Post.published.filter(category=post.category).exclude(pk=post.pk)[:3]

    return render(request, "blog/detail.html", {
        "post": post,
        "related_posts": related,
    })


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.published.filter(category=category)
    paginator = Paginator(posts, 9)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "blog/category.html", {
        "category": category,
        "page_obj": page_obj,
        "categories": Category.objects.all(),
    })
