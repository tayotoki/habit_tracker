from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from habits.views import HabitViewSet

if settings.API_DOCS_ENABLE:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("habits", HabitViewSet, basename="habits")
