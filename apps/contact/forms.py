from django import forms
from django.utils.translation import gettext_lazy as _
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    honeypot = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
        label="",
    )

    class Meta:
        model = ContactMessage
        fields = ["full_name", "email", "phone", "company", "subject", "message"]
        widgets = {
            "full_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": _("Votre nom complet"),
                "autocomplete": "name",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": _("votre@email.com"),
                "autocomplete": "email",
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": _("+225 XX XX XX XX XX"),
                "autocomplete": "tel",
                "inputmode": "tel",
            }),
            "company": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": _("Votre entreprise (optionnel)"),
                "autocomplete": "organization",
            }),
            "subject": forms.Select(attrs={"class": "form-control"}),
            "message": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 6,
                "placeholder": _("Décrivez votre projet ou votre demande..."),
            }),
        }

    def clean_honeypot(self):
        value = self.cleaned_data.get("honeypot", "")
        if value:
            raise forms.ValidationError("Détection de spam.")
        return value

    def clean_message(self):
        message = self.cleaned_data.get("message", "")
        if len(message.strip()) < 20:
            raise forms.ValidationError(_("Votre message est trop court (minimum 20 caractères)."))
        return message
