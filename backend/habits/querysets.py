from django.db.models import QuerySet


class HabitsQuerySet(QuerySet):
    """
    Менеджер привычек
    """

    def nice(self):
        """Приятные привычки"""
        return self.filter(is_nice=True)

    def useful(self):
        """Полезные привычки"""
        return self.filter(is_nice=False)

    def public(self):
        """С публичным статусом"""
        return self.filter(is_public=True)

    def private(self):
        """Приватные"""
        return self.filter(is_public=False)
