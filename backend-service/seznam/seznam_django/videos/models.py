from django.db import models


class Video(models.Model):
    name = models.CharField(max_length=1024)
    short_name = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)
