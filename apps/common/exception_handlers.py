from rest_framework.views import exception_handler
from .responses import CustomErrorResponse


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response.status_code == 403:
        exc_list = str(exc).split("DETAIL: ")
        return CustomErrorResponse({"message": exc_list[-1]}, status=403)
    elif response.status_code == 400:
        return CustomErrorResponse({"message": "Invalid Entry", "data": exc.detail})
