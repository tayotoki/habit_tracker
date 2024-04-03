from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager


class UserQuerySet(UserManager):
    """
    Менеджер пользователя
    """


class User(AbstractUser):
    """
    Пользователь
    """

    objects: UserQuerySet = UserQuerySet()

    chat_id = models.CharField(
        verbose_name="ID пользователя telegram",
        max_length=128,
        null=True,
        blank=True
    )

    def __str__(self) -> str:
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
