from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = "apps.accounts"
    verbose_name = "Comptes & Utilisateurs"

    def ready(self):
        import apps.accounts.signals  # noqa: F401
