from rest_framework import serializers

from .models import Habit


class HabitSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Habit
        fields = "__all__"

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data=validated_data)
