from django.contrib.admin import AdminSite


class DastAdminSite(AdminSite):
    site_header = "DAST NEWGEN'SPARK"
    site_title = "DAST Administration"
    index_title = "Tableau de bord"
    site_url = "/"
    enable_nav_sidebar = True
