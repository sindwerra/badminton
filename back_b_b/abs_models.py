from django.db import models


class BaseModel(models.Model):
    deleted = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True, blank=True)
    modified_on = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract = True