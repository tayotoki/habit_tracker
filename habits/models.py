from datetime import timedelta
from django.db import models
from django.db.models import Q, CheckConstraint

from users.models import User

from .constants import HabitPeriodicity


class Action(models.Model):
    name = models.CharField("Название действия")
    description = models.TextField(
        "Описание привычки", null=True, blank=True, help_text="Можно оставить пустым"
    )
    habit = models.ForeignKey(
        "Habit",
        on_delete=models.CASCADE,
        verbose_name="Привыяка",
        related_name="actions",
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Действие для привычки"
        verbose_name_plural = "Действия для привычек"


class Habit(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.CASCADE,
        related_name="habits",
    )
    place = models.CharField(verbose_name="Место выполнения", max_length=64)
    is_nice = models.BooleanField(verbose_name="Приятная", default=False)
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        verbose_name="Связанная приятная привычка",
        related_name="useful_habits",
        null=True,
        blank=True,
    )
    periodicity = models.PositiveSmallIntegerField(
        verbose_name="Периодичность",
        choices=HabitPeriodicity.choices,
        default=HabitPeriodicity.DAY,
    )
    reward = models.CharField(
        verbose_name="Награда", max_length=128, null=True, blank=True
    )
    time = models.DurationField(verbose_name="Время на выполнение", default=timedelta())
    is_public = models.BooleanField(verbose_name="Публичный доступ", default=False)

    def __str__(self) -> str:
        return f"{self.id} | {self.user} | {'Полезная' if not self.is_nice else 'Приятная'} | {self.get_periodicity_display()}"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        constraints = [
            # если is_nice=True, то related_habit должен быть null
            CheckConstraint(
                check=Q(is_nice=True, related_habit__isnull=True) | Q(is_nice=False),
                name="habit_nice_no_related_habit",
                violation_error_message=(
                    "У приятной привычки не может быть "
                    "связанной еще одной приятной привычки"
                ),
            ),
            # не может быть одновременно указаны related_habit и reward
            CheckConstraint(
                check=~Q(related_habit__isnull=False, reward__isnull=False),
                name="habit_no_related_habit_and_reward_together",
                violation_error_message=(
                    "В качестве награды может быть что-то одно: "
                    "приятная привычка или награда"
                ),
            ),
        ]
