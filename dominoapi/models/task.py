from django.db import models
from django.contrib.auth.models import User
from .list import List

class Task(models.Model):

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, null=True)
    is_complete = models.BooleanField()
    task_list = models.ForeignKey(List, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    importance = models.IntegerField(null=True)
    recurring = models.DateTimeField(null=True)

    class Meta:
        ordering = ("task_list",)

    def __str__(self):
        return self.name