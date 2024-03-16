from django.db.models import IntegerChoices


class HabitPeriodicity(IntegerChoices):
    DAY = 1, "раз в день"
    WEEK = 7, "раз в неделю"
    MONTH = 30, "раз в месяц"
