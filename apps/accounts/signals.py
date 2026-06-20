"""Auto-create the owner account on first run if configured via .env."""
import os
import logging
from django.db.models.signals import post_migrate
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_migrate)
def create_owner_account(sender, **kwargs):
    if sender.name != "apps.accounts":
        return

    from .models import User

    username = os.environ.get("SUPER_ADMIN_USERNAME", "dast_owner")
    email = os.environ.get("SUPER_ADMIN_EMAIL", "dastnewgenspark@gmail.com")
    password = os.environ.get("SUPER_ADMIN_PASSWORD", "")
    first_name = os.environ.get("SUPER_ADMIN_FIRST_NAME", "SABY")
    last_name = os.environ.get("SUPER_ADMIN_LAST_NAME", "Ange Noël")

    if not password:
        return

    if not User.objects.filter(is_owner=True).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_owner=True,
            role_title="Responsable & Propriétaire",
        )
        logger.info("Compte propriétaire DAST créé : %s", username)
