import pytest
from django.urls import reverse
from rest_framework import status
from unittest.mock import patch

from .factories import UserFactory, HabitFactory
from .fixtures import bad_habits_fixture, good_habits_fixture


@pytest.mark.django_db
class TestHabitViewSet:
    def test_list(self, api_client, django_assert_max_num_queries):
        user = UserFactory()
        api_client.force_authenticate(user)
        habits = [HabitFactory(user=user) for _ in range(3)]
        with django_assert_max_num_queries(3):
            api_client.get(reverse("habits-list"))

        response = api_client.get(reverse("habits-list"))

        assert response.status_code == status.HTTP_200_OK

        res_json = response.json()

        assert res_json["count"] == 3
        res_json = response.json()["results"]
        assert res_json[0]["id"] == habits[0].id
        assert res_json[1]["id"] == habits[1].id
        assert res_json[2]["id"] == habits[2].id
        assert res_json[0]["user"] == res_json[1]["user"] == res_json[2]["user"] == user.username

    def test_retrieve(self, api_client, django_assert_max_num_queries):
        user = UserFactory()
        api_client.force_authenticate(user)
        habits = [HabitFactory(user=user) for _ in range(3)]
        with django_assert_max_num_queries(3):
            api_client.get(reverse("habits-detail", kwargs={"pk": habits[0].id}))

        response = api_client.get(reverse("habits-detail", kwargs={"pk": habits[1].id}))
        assert response.status_code == status.HTTP_200_OK
        res_json = response.json()

        assert "id" in res_json
        assert "user" in res_json
        assert "place" in res_json
        assert "is_nice" in res_json
        assert "related_habit" in res_json
        assert "periodicity" in res_json
        assert "reward" in res_json
        assert "time" in res_json
        assert "is_public" in res_json
        assert "actions" in res_json
        assert isinstance(res_json["actions"], list)

    def test_create(self, api_client, bad_habits_fixture, good_habits_fixture):
        user = UserFactory()
        api_client.force_authenticate(user)

        for habit_data in good_habits_fixture:
            response = api_client.post(reverse("habits-list"), data=habit_data, format="json")
            assert response.status_code == status.HTTP_201_CREATED

        for habit_data in bad_habits_fixture:
            response = api_client.post(reverse("habits-list"), data=habit_data, format="json")
            assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_update(self, api_client):
        user = UserFactory()
        api_client.force_authenticate(user)

        habit = HabitFactory(user=user)
        habit_data = {
            "place": habit.place,
            "is_nice": habit.is_nice,
            "related_habit": habit.related_habit,
            "periodicity": habit.periodicity,
            "reward": habit.reward,
            "time": habit.time,
            "is_public": habit.is_public,
        }
        action = {
            **habit_data,
            "actions": [
                {
                    "name": "test_name"
                }
            ]
        }

        response = api_client.patch(
            reverse("habits-detail", kwargs={"pk": habit.pk}), data=action, format="json"
        )
        assert response.status_code == status.HTTP_200_OK
        # В ответе возвращается и поле 'description'
        action["actions"] = [
            {
                "name": "test_name",
                "description": None
            }
        ]
        assert response.json()["actions"] == action["actions"]

    @patch("habits.views.habits_notify.delay")
    def test_notify_user(self, mock_delay, api_client):
        user = UserFactory()
        api_client.force_authenticate(user=user)
        habit = HabitFactory(user=user)

        mock_delay.return_value = None

        response = api_client.post(reverse("habits-notify-user"))
        assert response.status_code == status.HTTP_200_OK
