# -*- coding: utf-8 -*-
from src.dj_project.app_settings import app_settings  # noqa     # isort:skip


gconfig = app_settings.create_gunicorn_config()

locals().update(gconfig)
