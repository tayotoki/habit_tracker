from django.db.models import QuerySet

from .models import Habit


def configure_telegram_message(habits: QuerySet[Habit]) -> str:
    message = "Ваши полезные привычки:\n\n"

    for habit in habits:
        reward = (
            [action.name for action in habit.related_habit.actions.all()]
            if habit.related_habit else habit.reward
        )
        message += (
            f"Место: {habit.place}\n"
            f"Периодичность: {habit.periodicity} дн.\n"
            f"Время выполнения: {habit.time}\n"
            f"Действия: {[action.name for action in habit.actions.all()]}\n"
            f"Награда: {reward}\n"
            f"\n"
        )

    return message
