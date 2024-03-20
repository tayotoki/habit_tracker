from django.db.models import QuerySet


class HabitsQuerySet(QuerySet):
    """
    Менеджер привычек
    """

    def nice(self):
        return self.filter(is_nice=True)

    def useful(self):
        return self.filter(is_nice=False)

    def public(self):
        return self.filter(is_public=True)

    def private(self):
        return self.filter(is_public=False)
