from django.db import models
from django.utils.timezone import now


class Entry(models.Model):
    title = models.CharField(max_length=64)
    text = models.TextField()
    created_at = models.DateTimeField(default=now)

    def __unicode__(self):
        return self.title
