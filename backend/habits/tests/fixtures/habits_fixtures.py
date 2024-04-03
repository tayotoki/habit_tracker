from unittest.mock import patch

import pytest
import json

from ..factories import HabitFactory


@pytest.fixture
def bad_habits_fixture():
    related_habit = HabitFactory(
        place="Home",
        is_nice=True,
        related_habit=None,
        periodicity=4,
        reward=None,
        time="00:01:00",
        is_public=True,
    )
    bad_habits = [
        {
            "place": "Gym",
            "is_nice": True,
            "related_habit": None,
            "periodicity": "string",
            "reward": "Ice cream",
            "time": "Evening",
            "is_public": True,
            "actions": []
        },
        {
            "place": "Gym",
            "is_nice": True,
            "related_habit": None,
            "periodicity": 2,
            "reward": "Ice cream",
            "time": "00:03:00",
            "is_public": True,
            "actions": []
        },
        {
            "place": "Gym",
            "is_nice": False,
            "related_habit": related_habit.id,
            "periodicity": 2,
            "reward": "test_string",
            "time": "00:02:00",
            "is_public": True,
            "actions": []
        }
    ]

    return bad_habits


@pytest.fixture
def good_habits_fixture():
    related_habit = HabitFactory(
        place="Home",
        is_nice=True,
        related_habit=None,
        periodicity=4,
        reward=None,
        time="00:01:00",
        is_public=True,
    )
    good_habits = [
        {
            "place": "Gym",
            "is_nice": False,
            "related_habit": related_habit.id,
            "periodicity": 7,
            "reward": None,
            "time": "00:01:40",
            "is_public": True,
            "actions": [
                {
                    "name": "test_action_1"
                },
                {
                    "name": "test_action_2"
                }
            ]
        },
    ]

    return good_habits
