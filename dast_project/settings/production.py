"""DAST NEWGEN'SPARK — Production Settings"""
from .base import *

DEBUG = False

ALLOWED_HOSTS = os.environ.get(
    "ALLOWED_HOSTS",
    "dastdigital.com,www.dastdigital.com"
).split(",")

SITE_URL = os.environ.get("SITE_URL", "https://dastdigital.com")

CSRF_TRUSTED_ORIGINS = [
    "https://dastdigital.com",
    "https://www.dastdigital.com",
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

# Supabase Storage for media in production
if os.environ.get("USE_SUPABASE_STORAGE") == "True":
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
    AWS_S3_ENDPOINT_URL = os.environ.get("AWS_S3_ENDPOINT_URL")
    AWS_STORAGE_BUCKET_NAME = os.environ.get("SUPABASE_STORAGE_BUCKET", "dast-media")
    AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", "auto")
    AWS_DEFAULT_ACL = "public-read"
    AWS_QUERYSTRING_AUTH = False
    AWS_S3_FILE_OVERWRITE = False
    MEDIA_URL = f"{AWS_S3_ENDPOINT_URL}/{AWS_STORAGE_BUCKET_NAME}/"

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
