# -*- coding: utf-8 -*-
import multiprocessing
import os
from typing import Optional
from pydantic_settings import BaseSettings
import ujson


class GunicornSetting(BaseSettings):
    GUNICORN_HOST: str = '0.0.0.0'
    GUNICORN_PORT: str = '5000'
    GUNICORN_BIND_PATH: Optional[str] = None
    GUNICORN_WORKER_CONCURRENCY: Optional[int] = 4

    GUNICORN_ACCESS_LOG: Optional[str] = '-'    # default log to console
    GUNICORN_ERROR_LOG: Optional[str] = '-'     # default log to console

    class Config:
        case_sensitive = True
        validate_assignment = True

    def create_gunicorn_config(self):
        # create gunicorn directory if neccessary
        log_dir = os.path.join(os.getcwd(), 'log', 'gunicorn')
        _worker_tmp_dir = os.path.join(os.getcwd(), 'log', 'gunicorn', 'tmp')
        for i in (log_dir, _worker_tmp_dir):
            if not os.path.isdir(i):
                os.makedirs(i)

        workers_per_core_str = os.getenv("WORKERS_PER_CORE", "1")
        max_workers_str = os.getenv("MAX_WORKERS")
        use_max_workers = None
        if max_workers_str:
            use_max_workers = int(max_workers_str)

        web_concurrency_str = os.getenv(
            "GUNICORN_WORKER_CONCURRENCY", self.GUNICORN_WORKER_CONCURRENCY)

        host = os.getenv("HOST", self.GUNICORN_HOST)
        port = os.getenv("PORT", self.GUNICORN_PORT)
        bind_env = os.getenv("GUNICORN_BIND_PATH", self.GUNICORN_BIND_PATH)

        if bind_env:
            use_bind = bind_env
        else:
            use_bind = f"{host}:{port}"

        cores = multiprocessing.cpu_count()
        workers_per_core = float(workers_per_core_str)
        default_web_concurrency = workers_per_core * cores
        if web_concurrency_str:
            web_concurrency = int(web_concurrency_str)
            assert web_concurrency > 0
        else:
            web_concurrency = max(int(default_web_concurrency), 2)
            if use_max_workers:
                web_concurrency = min(web_concurrency, use_max_workers)

        graceful_timeout_str = os.getenv("GRACEFUL_TIMEOUT", "120")
        timeout_str = os.getenv("TIMEOUT", "500")
        keepalive_str = os.getenv("KEEP_ALIVE", "120")

        # Gunicorn config variables
        workers = web_concurrency
        bind = use_bind
        errorlog = '-'
        worker_tmp_dir = _worker_tmp_dir
        accesslog = None
        graceful_timeout = int(graceful_timeout_str)
        timeout = int(timeout_str)
        keepalive = int(keepalive_str)
        limit_request_line = 0

        # gunicorn config
        gconfig = {
            "loglevel": "error",
            "workers": workers,
            "bind": bind,
            "graceful_timeout": graceful_timeout,
            "timeout": timeout,
            "keepalive": keepalive,
            "errorlog": errorlog,
            "accesslog": accesslog,
            'access_log_format': '{"time": "%(t)s", "name": "gunicorn", "method": "%(m)s", "url_path": "%(U)s", "status_code": "%(s)s", "length": %(B)s, "req_time": %(M)s}',
            # capture_output = True,        # capture print or other to error log       # NOSONAR
            'worker_tmp_dir': worker_tmp_dir,
            'limit_request_line': limit_request_line,
            # Additional, non-gunicorn variables
            "workers_per_core": workers_per_core,
            "use_max_workers": use_max_workers,
            "host": host,
            "port": port,
        }
        print(ujson.dumps(gconfig))
        print('Gunicorn Started with bind ', use_bind)

        return gconfig
