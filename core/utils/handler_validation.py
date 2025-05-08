import logging
import traceback

from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework.views import set_rollback
from django.http import response
from core import constants

logger = logging.getLogger(constants.CONSOLE_LOGGER)


class CustomValidationError(Exception):
    def __init__(self, code=200, message="", data=None):
        self.detail = {"code": code, "message": message, "data": data or {}}
        self.status_code = code


def custom_exception_handler(exc, context):
    if isinstance(exc, CustomValidationError):
        return Response(
            {
                "code": exc.detail["code"],
                "message": exc.detail["message"],
                "data": exc.detail.get("data", {}),
            },
            status=exc.status_code,
        )

    if isinstance(exc, exceptions.APIException):
        pass

    if isinstance(exc, response.Http404):
        return Response({"detail": "Not Found"}, status=404)

    if isinstance(exc, Exception):

        tb = traceback.TracebackException.from_exception(exc)
        frame = tb.stack[-1]
        logger.exception(
            f"Exception: {exc.__class__.__name__} - {exc} in {frame.name} at line {frame.lineno} in {frame.filename}"
        )

        set_rollback()

        return Response({"message": exc.__class__.__name__, "data": []}, status=500)

    return None
