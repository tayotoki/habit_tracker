from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import authentication, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import login, logout
from drf_spectacular.utils import extend_schema

from .models import User
from .serializers import UserSerializer
from .utils.decorators import only_register_action


@extend_schema(tags=["Users"])
class UserViewSet(mixins.CreateModelMixin, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def register(self, request):
        """Регистрация пользователя"""

        return self.create(request)

    @action(detail=False, methods=["POST"], permission_classes=[AllowAny])
    def auth(self, request):
        """Авторизация пользователя"""

        username = request.data.get("username")
        password = request.data.get("password")

        user = authentication.authenticate(
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return Response(
                {"success": "User authenticated successfully!"},
                status=status.HTTP_200_OK,
            )

        return Response(
            {"error": "Invalid username or password."},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    @extend_schema(request=None)
    @action(
        detail=False,
        methods=["POST"],
        permission_classes=[IsAuthenticated],
    )
    def logout(self, request):
        logout(request)
        return Response(
            {"success": "User logged out successfully"},
            status=status.HTTP_200_OK
        )

    @only_register_action
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
