from django.db import models


class Feature(models.Model):
    name = models.CharField(max_length=2048, unique=True)

class Drm(models.Model):
    name = models.CharField(max_length=2048, unique=True)


class Metadata(models.Model):
    name = models.CharField(max_length=2048)
    short_name = models.CharField(max_length=2048)
    icon_uri = models.CharField(max_length=2048)
    manifest_uri = models.CharField(max_length=2048)
    description = models.CharField(max_length=2048)
    is_featured = models.BooleanField()
    complete_json = models.JSONField()

    features = models.ManyToManyField('Feature')
    drms = models.ManyToManyField('Drm')


class FetchMetadata(models.Model):
    data_expires_at = models.DateTimeField(null=True)

    def save(self, *args, **kwargs) -> None:
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        object, _ = cls.objects.get_or_create(pk=1)
        return object
