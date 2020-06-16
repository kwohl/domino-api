from django.db import models

class Step(models.Model):

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250, null=True)
    is_complete = models.BooleanField()
    importance = models.IntegerField(null=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name