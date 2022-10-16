class BaseRepository:
    """Base class representing repository."""

    def __init__(self, klass):
        self.klass = klass

    def fetch(self, first=False, limit=None, **kwargs):
        qs = self.klass.objects.filter(**kwargs)
        if first:
            return qs.first()
        elif limit:
            return qs[:limit]
        return qs

    def create(self, **kwargs):
        return self.klass.objects.create(**kwargs)
