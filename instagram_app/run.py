"""Standalone launcher: python instagram_app/run.py"""
from pathlib import Path
import os
import sys

PROJECT_ROOT = Path(__file__).resolve().parent.parent
APP_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from django.conf import settings

if not settings.configured:
    settings.configure(
        DEBUG=True,
        BASE_DIR=PROJECT_ROOT,
        SECRET_KEY="roya-instagram-demo-local-only",
        ROOT_URLCONF="instagram_app.urls",
        ALLOWED_HOSTS=["127.0.0.1", "localhost"],
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.staticfiles",
            "roya",
        ],
        MIDDLEWARE=[
            "django.middleware.common.CommonMiddleware",
            "django.middleware.csrf.CsrfViewMiddleware",
        ],
        DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
        TEMPLATES=[{
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [APP_ROOT / "templates"],
            "APP_DIRS": True,
            "OPTIONS": {},
        }],
        STATIC_URL="/static/",
        USE_TZ=True,
        DEFAULT_AUTO_FIELD="django.db.models.AutoField",
    )

import django
django.setup()

from django.core.management import execute_from_command_line

if __name__ == "__main__":
    host = os.environ.get("ROYA_HOST", "127.0.0.1")
    port = os.environ.get("ROYA_PORT", "8090")
    execute_from_command_line(["instagram_app", "runserver", f"{host}:{port}", "--noreload"])
