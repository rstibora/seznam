from django.db import models


class Video(models.Model):
    name = models.CharField(max_length=1024)
    short_name = models.CharField(max_length=1024)
    description = models.CharField(max_length=1024)


class FetchMetadata(models.Model):
    data_expires_at = models.DateTimeField(null=True)

    def save(self, *args, **kwargs) -> None:
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        object, _ = cls.objects.get_or_create(pk=1)
        return object
