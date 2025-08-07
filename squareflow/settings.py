import os
from pathlib import Path
import dj_database_url

# ─── Caminhos básicos ─────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Configurações de segurança (dev) ─────────────────────────
SECRET_KEY   = "as155sa4dsa541das15sad1as5"
DEBUG        = True
ALLOWED_HOSTS = [
    "uniquetrack.onrender.com",
    "www.uniquetrack.onrender.com",   # se tiver
]

CSRF_TRUSTED_ORIGINS = [
    "https://uniquetrack.onrender.com",
    "https://www.uniquetrack.onrender.com",
    # ou genérico, se você tiver mais projetos
    "https://*.onrender.com",
]

# ─── Apps ─────────────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # terceiros
    "cloudinary",
    "cloudinary_storage",
    # seu app
    "core",
]

# ─── Middleware ───────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "squareflow.urls"
WSGI_APPLICATION = "squareflow.wsgi.application"

# ─── Banco de dados (Postgres na Render) ──────────────────────
DATABASES = {
    "default": dj_database_url.parse(
        "postgresql://uniquedb_hwty_user:nO90a6PQSa7phmDwGxhmKMksEx5bcTw4"
        "@dpg-d2a5s1ogjchc73e9gi20-a.oregon-postgres.render.com/uniquedb_hwty",
        conn_max_age=600,
        ssl_require=True,
    )
}

# ─── Templates ────────────────────────────────────────────────
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

# ─── Arquivos estáticos / mídia ───────────────────────────────
STATIC_URL   = "/static/"
STATIC_ROOT  = BASE_DIR / "staticfiles"
MEDIA_URL    = "/media/"
MEDIA_ROOT   = BASE_DIR / "media"

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": "SUA_CLOUD",
    "API_KEY":    "SUA_KEY",
    "API_SECRET": "SUA_SECRET",
}

# ─── Auth redirects ───────────────────────────────────────────
LOGIN_URL          = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"

# ─── Outras opções ────────────────────────────────────────────
# Armazena mensagens Django na sessão (evita problemas de cookie cheio)
MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

#RHD6TWZFAJ9V7QMHGSM6R4BT
