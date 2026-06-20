from django.contrib.admin.apps import AdminConfig


class DastAdminConfig(AdminConfig):
    """
    Custom AdminConfig that wires Django's admin to our branded AdminSite.
    Registered in INSTALLED_APPS as 'dast_project.apps.DastAdminConfig'
    replacing 'django.contrib.admin'.
    """
    name = "django.contrib.admin"
    default_site = "dast_project.admin_site.DastAdminSite"
