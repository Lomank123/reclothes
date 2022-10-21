from django.db import models


class ActiveCartManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(
            is_archived=False, is_deleted=False)
