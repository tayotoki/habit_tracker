from django.db import IntegrityError
from rest_framework import viewsets, status
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .serializers import HabitSerializer
from .models import Habit
from .viewsets_mixins import catch_db_constraints


@extend_schema(tags=["Habits"])
@catch_db_constraints
class HabitViewSet(viewsets.ModelViewSet):
    queryset = Habit.objects.select_related("user").prefetch_related("actions")
    serializer_class = HabitSerializer
