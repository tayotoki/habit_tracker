from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser

from .models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data) -> AbstractBaseUser:
        user = get_user_model().objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )

        return user

    class Meta:
        model = User
        fields = ("username", "email", "password")
