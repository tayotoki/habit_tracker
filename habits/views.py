from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema, OpenApiResponse

from .serializers import HabitSerializer
from .models import Habit
from .viewsets_mixins import catch_db_constraints, paginate
from .tasks import habits_notify
from .pagination import CustomPageNumberPagination


@extend_schema(tags=["Habits"])
@catch_db_constraints
class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = CustomPageNumberPagination

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

    @extend_schema(request=None, responses={
            status.HTTP_200_OK: OpenApiResponse(
                response={"detail": "Notify is sending"},
                description="Отправка произошла успешно",
            ),
        })
    @action(detail=False, methods=["POST"])
    def notify_user(self, request, *args, **kwargs):
        """
        Уведомление пользователя на стороннем сервисе
        """

        habits_notify.delay(request.user.username)

        return Response(
            {"detail": "Notify is sending"},
            status=status.HTTP_200_OK
        )
