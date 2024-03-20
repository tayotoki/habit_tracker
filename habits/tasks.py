from celery import shared_task

from .models import Habit
from .services import TelegramBotService


@shared_task
def habits_remind():
    print("Habbit remind was sended")


@shared_task
def habits_notify(username):
    habits_qs = (
        Habit.objects
        .filter(user__username=username)
        .prefetch_related("actions")
        .select_related("related_habit", "related_habit__actions")
        .useful()
    )

    message = "Ваши полезные привычки:\n"

    for habit in habits_qs:
        reward = (
            [action.name for action in habit.related_habit.actions.all()]
            if habit.related_habit else habit.reward
        )
        message += (
            f"Место: {habit.place}\n"
            f"Периодичность: {habit.periodicity} дн.\n"
            f"Время выполнения: {habit.time}\n"
            f"Награда: {reward}\n"
            f"\n"
        )

    service = TelegramBotService(username=username)

    service.send_message(message=message)
