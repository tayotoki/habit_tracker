import inspect
import functools

from rest_framework.response import Response
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED


def only_register_action(method):
    """
    Вызывать данный метод можно только
    в методе register
    """

    @functools.wraps(method)
    def wrapper(view_cls, *args, **kwargs):
        current_frame = inspect.currentframe()
        caller_frame = current_frame.f_back
        code_obj = caller_frame.f_code
        code_obj_name = code_obj.co_name

        if code_obj_name == view_cls.register.__name__:
            return method(view_cls, *args, **kwargs)
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)

    return wrapper
