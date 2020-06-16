from django.db import models
from .step import Step
from .task import Task

class TaskStep(models.Model):

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    step = models.ForeignKey(Step, on_delete=models.CASCADE)

