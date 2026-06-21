"""DAST NEWGEN'SPARK — Production Settings"""
from .base import *

DEBUG = False

ALLOWED_HOSTS = os.environ.get(
    "ALLOWED_HOSTS",
    "dastdigital.com,www.dastdigital.com"
).split(",")

# Ajouter automatiquement l'URL de preview Vercel (unique par déploiement)
_vercel_url = os.environ.get("VERCEL_URL", "")
if _vercel_url and _vercel_url not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(_vercel_url)

# Autoriser tous les sous-domaines *.vercel.app pour les previews
ALLOWED_HOSTS.append(".vercel.app")

SITE_URL = os.environ.get("SITE_URL", "https://dastdigital.com")

CSRF_TRUSTED_ORIGINS = [
    "https://dastdigital.com",
    "https://www.dastdigital.com",
    "https://*.vercel.app",
] + [
    f"https://{h.strip()}"
    for h in os.environ.get("ALLOWED_HOSTS", "").split(",")
    if h.strip() and h.strip() not in ("dastdigital.com", "www.dastdigital.com")
]

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
# Vercel / proxy gèrent le HTTPS en amont — pas de redirection interne
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Supabase Storage for media in production (Django 4.2+ STORAGES format)
if os.environ.get("USE_SUPABASE_STORAGE") == "True":
    _s3_endpoint = os.environ.get("AWS_S3_ENDPOINT_URL", "")
    _s3_bucket = os.environ.get("SUPABASE_STORAGE_BUCKET", "dast-media")
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
            "OPTIONS": {
                "access_key": os.environ.get("AWS_ACCESS_KEY_ID"),
                "secret_key": os.environ.get("AWS_SECRET_ACCESS_KEY"),
                "endpoint_url": _s3_endpoint,
                "bucket_name": _s3_bucket,
                "region_name": os.environ.get("AWS_S3_REGION_NAME", "eu-central-1"),
                "default_acl": "public-read",
                "querystring_auth": False,
                "file_overwrite": False,
            },
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
        },
    }
    MEDIA_URL = f"{_s3_endpoint}/{_s3_bucket}/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
