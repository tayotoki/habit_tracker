from rest_framework import serializers

from .models import Habit, Action


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = (
            "name",
            "description",
        )


class HabitSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    actions = ActionSerializer(many=True)

    class Meta:
        model = Habit
        fields = (
            "id",
            "user",
            "place",
            "is_nice",
            "related_habit",
            "periodicity",
            "reward",
            "time",
            "is_public",
            "actions",
        )

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        actions_data = validated_data.pop("actions")
        habit = Habit.objects.create(**validated_data)
        for action in actions_data:
            Action.objects.create(habit=habit, **action)
        return habit

    def update(self, instance, validated_data):
        instance.place = validated_data.get("place", instance.place)
        instance.is_nice = validated_data.get("is_nice", instance.is_nice)
        instance.related_habit = validated_data.get(
            "related_habit", instance.related_habit
        )
        instance.periodicity = validated_data.get("periodicity", instance.periodicity)
        instance.reward = validated_data.get("reward", instance.reward)
        instance.time = validated_data.get("time", instance.time)
        instance.is_public = validated_data.get("is_public", instance.is_public)

        actions_data = validated_data.get("actions", [])
        instance.actions.all().delete()

        for action_data in actions_data:
            Action.objects.create(habit=instance, **action_data)

        instance.save()

        return instance
