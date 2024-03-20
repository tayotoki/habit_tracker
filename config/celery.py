import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery(broker=settings.CELERY_BROKER_URL)
app.config_from_object("django.conf:settings")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "remind_for_all_habits": {
        "task": "habits.tasks.habits_remind",
        "schedule": crontab(hour="8"),
        "options": {"queue": "habits_periodic"},
    }
}
