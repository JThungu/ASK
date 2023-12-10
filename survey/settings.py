import os
from pathlib import Path
from decouple import config

#BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
SECRET_KEY = config('SECRET_KEY', default='your_default_secret_key')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = []
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "survey",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": [
            "profile",
            "email",
            "openid"
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
        "APP": {
            "client_id": config('GOOGLE_CLIENT_ID', default='your_default_client_id'),
            "secret": config('GOOGLE_CLIENT_SECRET', default='your_default_client_secret'),
            "redirect_uris": ["http://localhost:8000/accounts/google/login/callback/"],
        }
    }
}
MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]
ROOT_URLCONF = "survey.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
WSGI_APPLICATION = "survey.wsgi.application"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]
AUTHENTICATION_BACKENDS = [
    "allauth.account.auth_backends.AuthenticationBackend",
]
STATIC_URL = '/static/'
#STATICFILES_DIRS = [
#    BASE_DIR / "staticfiles",
#]
STATIC_ROOT = BASE_DIR / "staticfiles"
# Django Allauth settings
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True
#STATIC_URL = "/static/"
#STATICFILES_DIRS = []
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/surveys/"
INTERNAL_IPS = ["127.0.0.1"]

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='your_default_email_username')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='your_default_email_password')
DEFAULT_FROM_EMAIL = "testdev161@gmail.com"
try:
    from .local_settings import *
except ImportError:
    pass
