from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import User


def team_page(request):
    members = User.objects.filter(show_on_team_page=True, is_active=True).order_by("team_order", "first_name")
    return render(request, "accounts/team.html", {"members": members})
