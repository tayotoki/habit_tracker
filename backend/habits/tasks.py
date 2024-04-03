from celery import shared_task

from .models import Habit
from .services import TelegramBotService
from .utils import configure_telegram_message


@shared_task
def habits_remind():
    print("Habit remind was sended")


@shared_task
def habits_notify(username):
    habits_qs = (
        Habit.objects
        .filter(user__username=username)
        .select_related("related_habit")
        .prefetch_related("actions", "related_habit__actions")
        .useful()
    )

    message = configure_telegram_message(habits=habits_qs)

    service = TelegramBotService(username=username)

    service.send_message(message=message)
