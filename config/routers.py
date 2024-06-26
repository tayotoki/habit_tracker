from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from habits.views import HabitViewSet
from users.views import UserViewSet

if settings.API_DOCS_ENABLE:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("habits", HabitViewSet, basename="habits")
router.register("users", UserViewSet, basename="users")
