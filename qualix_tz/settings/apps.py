import typing

# Application definition
INSTALLED_APPS: typing.Final = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "request_sender",
]

__all__ = [
    "INSTALLED_APPS",
]
