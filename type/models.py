from django.db import models


class Type(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return f"{self.name}"
