from django.db import models


class TaskProgress(models.Model):
    task_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='task_id'
    )

    total = models.IntegerField(
        default=100
    )
    progress = models.IntegerField(
        default=0
    )
    step = models.CharField(
        max_length=255,

    )
