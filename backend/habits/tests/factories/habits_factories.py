from datetime import timedelta

from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from habits.constants import HabitPeriodicity
from habits.models import Action, Habit
from .user_factory import UserFactory


class ActionFactory(DjangoModelFactory):
    class Meta:
        model = Action

    name = Faker("word")
    description = Faker("text")
    habit = SubFactory("habits.tests.factories.HabitFactory")


class HabitFactory(DjangoModelFactory):
    class Meta:
        model = Habit

    user = SubFactory(UserFactory)
    place = Faker("city")
    is_nice = Faker("boolean")
    related_habit = None
    periodicity = HabitPeriodicity.DAY
    reward = Faker("sentence")
    time = timedelta(seconds=60)
    is_public = Faker("boolean")
