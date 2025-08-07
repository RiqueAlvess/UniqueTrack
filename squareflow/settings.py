import os
from pathlib import Path

# ──────────────────────────────────────────────────────────────
# CAMINHOS BÁSICOS
# ──────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ──────────────────────────────────────────────────────────────
# APPS INSTALADOS
# ──────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Terceiros
    "cloudinary",
    "cloudinary_storage",

    # Seu app
    "core",
]

# ──────────────────────────────────────────────────────────────
# USUÁRIOS / AUTH
# ──────────────────────────────────────────────────────────────
AUTH_USER_MODEL = "auth.User"  # caso mude no futuro

# ──────────────────────────────────────────────────────────────
# MIDDLEWARE
# ──────────────────────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ──────────────────────────────────────────────────────────────
# URL / WSGI
# ──────────────────────────────────────────────────────────────
ROOT_URLCONF = "squareflow.urls"
WSGI_APPLICATION = "squareflow.wsgi.application"

# ──────────────────────────────────────────────────────────────
# TEMPLATES (Bootstrap toasts dependem do context-processor messages)
# ──────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# ──────────────────────────────────────────────────────────────
# DATABASE – SQLite para dev; troque em produção
# ──────────────────────────────────────────────────────────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ──────────────────────────────────────────────────────────────
# STATIC / MEDIA
# ──────────────────────────────────────────────────────────────
STATIC_URL = "/static/"
MEDIA_URL = "/media/"

STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_ROOT = BASE_DIR / "media"

# Cloudinary para imagens de relatórios
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": "SUA_CLOUD",
    "API_KEY": "SUA_KEY",
    "API_SECRET": "SUA_SECRET",
}

# ──────────────────────────────────────────────────────────────
# LOGIN / LOGOUT
# ──────────────────────────────────────────────────────────────
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"

# ──────────────────────────────────────────────────────────────
# DIVERSOS
# ──────────────────────────────────────────────────────────────
ALLOWED_HOSTS = ["*"]   # ajuste em produção
DEBUG = True            # False em produção
SECRET_KEY = "as155sa4dsa541das15sad1as5"  # gere um novo em produção
