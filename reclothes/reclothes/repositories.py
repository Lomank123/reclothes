class BaseRepository:
    """Base class representing repository."""

    def __init__(self, model):
        self.model = model

    def fetch(self, first=False, limit=None, **kwargs):
        qs = self.model.objects.filter(**kwargs)
        if first:
            return qs.first()
        elif limit:
            return qs[:limit]
        return qs

    def create(self, **kwargs):
        return self.model.objects.create(**kwargs)
