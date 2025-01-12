from django.db import models
from django.utils.timezone import now


class DateTimeBasedModel(models.Model):
    created = models.DateTimeField(default=now, editable=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created']