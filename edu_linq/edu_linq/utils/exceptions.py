from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status


def exception_handler(exc, context):
    error = "%s %s %s" % (context["view"], context["request"].method, exc)
    response = drf_exception_handler(exc, context)
    if response is None:
        return Response({"error_message": "出错了..."},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return response
