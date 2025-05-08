import logging
import time
import traceback
from typing import Dict
from django.http import HttpRequest, HttpResponse
from core.constants import CONSOLE_LOGGER
from core.utils.thread_local import elog, EventLogging


class EventLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.event_logging: EventLogging = elog
        self.logger = logging.getLogger(CONSOLE_LOGGER)

    def _get_request_headers_for_logging(self, request: HttpRequest):
        headers = {'my-tracking': 'zinc-request'}
        return headers

    def _get_response_headers_for_logging(self, response: HttpResponse):
        headers = {'my-tracking': 'zinc-request'}
        return headers

    def _log_request(
        self,
        eid: str, method: str,
        url_path: str,
        headers: Dict,
        **kwargs
    ):
        log_extra = {
            'eid': eid,
            'req_url': url_path,
            'req_method': method,
            'req_headers': headers,
        }
        self.logger.info(f'new request: {method} {url_path}', extra=log_extra)

    def _get_response_content(self, response: HttpResponse):
        resp_content = ''
        if not isinstance(response, HttpResponse):
            return resp_content
        try:
            if response.content:
                if isinstance(resp_content, bytes):
                    resp_content = response.content.decode('utf-8')
                else:
                    resp_content = str(response.content)
        except Exception as e:
            print('error in decoding response content loc=0cor0016', e)
            resp_content = ''
        finally:
            return resp_content

    def _log_response(
        self,
        eid: str,
        method: str,
        url_path: str,
        status_code: int,
        timing: int,
        headers: Dict,
        **kwargs
    ):
        log_extra = {
            'eid': eid,
            'timing': timing,
            'resp_status': status_code,
            'resp_headers': headers,
        }
        current_exception = self.event_logging.get_current_exc()
        if current_exception:
            try:
                _traceback_frames = traceback.format_exception(
                    current_exception
                )
                log_extra['resp_exception'] = ' '.join(_traceback_frames)
            except Exception as e:
                log_extra['resp_exception'] = f'midleware-event-log -> {e}'
        if status_code >= 400:
            log_extra['resp_content'] = self._get_response_content(
                kwargs.get('response', None))

        self.logger.info(
            f'response: {method} {url_path} {status_code} {timing}', extra=log_extra)

    def __call__(self, request: HttpRequest):
        # mark this is new request
        self.event_logging.handle_new_request()

        # collect request data
        eid = self.event_logging.get_event_id()
        start_time = time.time_ns()
        method = request.method
        url_path = request.get_full_path()
        request_headers = self._get_request_headers_for_logging(request)

        # log request
        self._log_request(eid, method, url_path, request_headers)

        # handle request, make response
        try:
            response: HttpResponse = self.get_response(request)
        except Exception:
            raise
        finally:
            # log response
            # must put in finally to log response even if exception is raised
            response_headers = self._get_response_headers_for_logging(response)
            self._log_response(
                eid,
                method,
                url_path,
                response.status_code,
                time.time_ns() - start_time,
                response_headers,
                response=response
            )
        # always return response
        return response

    def process_exception(self, request, exception):
        self.event_logging.set_current_exc(exception)
        self.logger.exception(f'get exception {exception}')
        # do nothing, let the other middleware handle the exception
