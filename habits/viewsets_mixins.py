import functools

from django.db import IntegrityError
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.response import Response

from .models import Habit

models_to_watch = [
    Habit,
]

constraints = []

for model in models_to_watch:
    constraints.extend(model._meta.constraints)


CONSTRAINTS = {constraint.name: constraint for constraint in constraints}


def try_handle(method):
    """
    Проверка методов на нарушение ограничений БД
    """

    @functools.wraps(method)
    def wrapper(viewset, *args, **kwargs):
        if method.__name__ in viewset.CATCH_IN:
            try:
                response = method(viewset, *args, **kwargs)
            except IntegrityError as e:
                detail = f"{e}"
                for name, instance in CONSTRAINTS.items():
                    if name in detail:
                        detail = instance.violation_error_message
                response = Response(
                    {
                        "detail": detail,
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )
            return response

    return wrapper


def catch_db_constraints(viewset):
    """
    Обработка ограничений модели из БД.
    """

    class ViewSetMixin(viewset):
        CATCH_IN: list[str] = ["create", "update", "partial_update"]

        @try_handle
        def create(self, *args, **kwargs):
            return viewset.create(self, *args, **kwargs)

        @try_handle
        def update(self, *args, **kwargs):
            return viewset.update(self, *args, **kwargs)

        @try_handle
        def partial_update(self, *args, **kwargs):
            return viewset.update(self, *args, **kwargs)

    return ViewSetMixin


def paginate(func):

    @functools.wraps(func)
    def inner(self, *args, **kwargs):
        queryset = func(self, *args, **kwargs)
        assert isinstance(queryset, (list, QuerySet))

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    return inner
