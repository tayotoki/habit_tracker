from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from drf_spectacular.utils import extend_schema

from .serializers import HabitSerializer
from .models import Habit
from .viewsets_mixins import catch_db_constraints, paginate


@extend_schema(tags=["Habits"])
@catch_db_constraints
class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = (
            Habit.objects
            .prefetch_related("actions")
            .select_related("related_habit")
        )

        match self.action:
            case self.list.__name__:
                queryset = (
                    queryset
                    .filter(user=self.request.user)
                    .select_related("user")
                )
            case self.public_habits.__name__:
                queryset = (
                    queryset
                    .public()
                    .select_related("user")
                )
            case self.retrieve.__name__:
                queryset = (
                    queryset
                    .filter(
                        user=self.request.user,
                        pk=self.kwargs["pk"]
                    )
                )

        return queryset

    @paginate
    @action(detail=False, methods=["GET"])
    def public_habits(self, request, *args, **kwargs):
        """
        Все публичные привычки пользователей
        """

        return self.get_queryset()
