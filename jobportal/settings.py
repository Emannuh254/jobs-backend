import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
from datetime import timedelta

# ===================================
# Load environment variables
# ===================================
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ===================================
# Security
# ===================================
SECRET_KEY = os.getenv("SECRET_KEY", "insecure-secret-key")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# ===================================
# Installed apps
# ===================================
INSTALLED_APPS = [
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    # Local apps
    "accounts",
    "jobs",
    "referrals",
    "applications",
]

# ===================================
# Middleware
# ===================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ===================================
# URL + WSGI
# ===================================
ROOT_URLCONF = "jobportal.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Add this line
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

WSGI_APPLICATION = "jobportal.wsgi.application"

# ===================================
# Database
# ===================================
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
        ssl_require=not DEBUG,
    )
}

# ===================================
# Password validation
# ===================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator", "OPTIONS": {"min_length": 8}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ===================================
# Internationalization
# ===================================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ===================================
# Static files
# ===================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# ===================================
# Primary key type
# ===================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ===================================
# CORS
# ===================================
# CORS
CORS_ALLOWED_ORIGINS = os.getenv(
    "CORS_ALLOWED_ORIGINS",
    "https://emannuh254.github.io,http://127.0.0.1:5500"
).split(",")

# CSRF trusted origins must include scheme
CSRF_TRUSTED_ORIGINS = [
    origin for origin in CORS_ALLOWED_ORIGINS if origin.startswith(("http://", "https://"))
]


# ===================================
# Django REST Framework
# ===================================
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

# ===================================
# JWT (SimpleJWT)
# ===================================
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.getenv("JWT_EXP_DAYS", 1))),
    "ROTATE_REFRESH_TOKENS": True,
}

# ===================================
# Custom user model
# ===================================
AUTH_USER_MODEL = "accounts.User"

# ===================================
# Google OAuth2
# ===================================
GOOGLE_OAUTH2_CLIENT_ID = os.getenv("GOOGLE_OAUTH2_CLIENT_ID", "")

# ===================================
# Email settings
# ===================================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'noreply@jobportal.com')

# ===================================
# Frontend URL
# ===================================
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://127.0.0.1:5500')

# ===================================
# Port
# ===================================
PORT = int(os.getenv("PORT", 8000))