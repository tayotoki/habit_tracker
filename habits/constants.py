from django.db.models import IntegerChoices


class HabitPeriodicity(IntegerChoices):
    DAY = 1, "раз в день"
    TWO_DAYS = 2, "раз в два дня"
    THREE_DAYS = 3, "раз в три дня"
    FOUR_DAYS = 4, "раз в четыре дня"
    FIVE_DAYS = 5, "раз в пять дней"
    SIX_DAYS = 6, "раз в шесть дней"
    WEEK = 7, "раз в неделю"
