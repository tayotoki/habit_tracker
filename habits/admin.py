from django.contrib import admin
from .models import Habit, Action


class ActionInline(admin.StackedInline):
    model = Action
    extra = 0
    classes = ["collapse"]


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    inlines = [ActionInline]
    exclude = ("actions",)
