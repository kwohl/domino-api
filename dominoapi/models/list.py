from django.db import models
from django.contrib.auth.models import User

class List(models.Model):

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name