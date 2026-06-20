from django.urls import path
from . import views

app_name = "contact"

urlpatterns = [
    path("", views.contact_view, name="index"),
    path("merci/", views.contact_success, name="success"),
]
