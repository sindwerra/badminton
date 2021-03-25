from django.db import models


class BaseModel(models.Model):
    deleted = models.IntegerField(default=0)

    class Meta:
        abstract = True