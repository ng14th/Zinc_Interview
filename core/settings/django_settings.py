# -*- coding: utf-8 -*-
from typing import Dict, List, Optional, Tuple

from .base_settings import BaseSettings


class DjangoSetting(BaseSettings):

    DJANGO_DEBUG: bool = False
    DJANGO_SECRET_KEY: Optional[str] = None
    DJANGO_SETTINGS_IMPORT: Optional[str] = 'src.dj_project.settings'

    DJANGO_USE_TZ: bool = False
    DJANGO_TIMEZONE: str = 'UTC'

    DJANGO_STATIC_URL: str = 'static/'
    DJANGO_MEDIA_URL: str = 'media/'
    DJANGO_ADMIN_URL: str = 'admin/'

    DJANGO_ALLOWED_HOSTS: List[str] = ['*']

    DJANGO_CORS_ALLOWED_ORIGINS: List[str] = []
    DJANGO_CORS_ALLOWED_METHOD: List[str] = []

    # debug apps, will be append to INSTALLED_APPS
    DJANGO_DEBUG_APPS: List[str] = []

    # django app utilities
    DJANGO_ALLOW_ASYNC_UNSAFE: bool = False
    DJANGO_EMAIL_BACKEND: str = 'django.core.mail.backends.smtp.EmailBackend'
    DJANGO_EMAIL_HOSTS: str = 'mailhog'
    DJANGO_EMAIL_PORT: int = 1025
    DJANGO_DEFAULT_FROM_EMAIL: str = "chat_service <noreply@portal.sop-fpt.online>"

    # django all-auth
    DJANGO_ACCOUNT_ALLOW_REGISTRATION: bool = True
    DJANGO_ACCOUNT_AUTHENTICATION_METHOD: str = 'username'

    #
    DJANGO_SECURE_PROXY_SSL_HEADER: Tuple[str, str] = (
        "HTTP_X_FORWARDED_PROTO", "https",)
    DJANGO_SECURE_SSL_REDIRECT: bool = False
    DJANGO_SESSION_COOKIE_SECURE: bool = True
    DJANGO_CSRF_COOKIE_SECURE: bool = True
    DJANGO_SECURE_HSTS_SECONDS: int = 60
    DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS: bool = True
    DJANGO_SECURE_HSTS_PRELOAD: bool = True
    DJANGO_SECURE_CONTENT_TYPE_NOSNIFF: bool = True
