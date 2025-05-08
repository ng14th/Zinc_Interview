from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers


def custom_response(status_code=status.HTTP_200_OK, message="", data=[]):
    return Response(
        {
            'status': status_code,
            'message': message,
            'data': data
        },
        status=status_code
    )


def custom_reponse_validate_error(sz: serializers.Serializer):
    messages = []
    for field, error in sz.errors.items():
        for detail in error:
            messages.append(f'{field} {detail}')
    err_msg = ','.join(messages)
    return custom_response(
        400,
        err_msg,
        {
            "message": err_msg
        }
    )
