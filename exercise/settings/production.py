import os

from pathlib import Path

from exercise.settings.base import *

# Force HTTPS
SECURE_SSL_REDIRECT = True

# Cookies only sent over HTTPS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

LOGS_DIR = Path("/exercise/logs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)  # create folder if it doesn't exist
LOG_FILE = LOGS_DIR / "django.log"

LOG_LEVEL = os.getenv("DJANGO_LOG_LEVEL", "INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} [{name}] {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(LOG_FILE),
            "formatter": "verbose",
            "encoding": "utf-8",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 0,
        },
    },
    "root": {
        "handlers": ["console", "file"],
        "level": LOG_LEVEL,
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file"],
            "level": LOG_LEVEL,
            "propagate": False,
        },
        "django.request": {
            "handlers": ["console", "file"],
            "level": "ERROR",  # logs HTTP 500 errors
            "propagate": False,
        },
    },
}
