from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
import logging

from .forms import ContactForm
from .models import ContactMessage

logger = logging.getLogger(__name__)


def contact_view(request):
    form = ContactForm()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
            msg.ip_address = x_forwarded.split(",")[0] if x_forwarded else request.META.get("REMOTE_ADDR")
            msg.save()

            _send_notification(msg)

            messages.success(request, "Votre message a bien été envoyé. Nous vous répondrons dans les plus brefs délais.")
            return redirect("contact:success")

    return render(request, "contact/index.html", {"form": form})


def contact_success(request):
    return render(request, "contact/success.html")


def _send_notification(msg: ContactMessage):
    """Send email notification to DAST team."""
    try:
        html_body = render_to_string("contact/email_notification.html", {"msg": msg})
        send_mail(
            subject=f"[DAST] Nouveau message — {msg.get_subject_display()} — {msg.full_name}",
            message=f"De : {msg.full_name} <{msg.email}>\nSujet : {msg.get_subject_display()}\n\n{msg.message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.CONTACT_EMAIL],
            html_message=html_body,
            fail_silently=False,
        )
    except Exception as exc:
        logger.error("DAST contact email ERROR: %s", exc, exc_info=True)
