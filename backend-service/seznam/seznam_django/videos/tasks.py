from datetime import datetime, timedelta, timezone

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
import requests

from videos.models import FetchMetadata, Metadata
from videos.serializers import FullMetadataSerializer


VIDEOS_URL = ("https://gist.githubusercontent.com/nextsux/f6e0327857c88caedd2dab13affb72c1"
              "/raw/04441487d90a0a05831835413f5942d58026d321/videos.json")


class FetchFailed(Exception):
    pass


def _update_metadata() -> None:
    response = requests.get(VIDEOS_URL)

    if not response.ok:
        raise FetchFailed("Could not fetch videos metadata.")

    for video_metadata in response.json():
        # Since there is no unique identifier in the json, it is assumed that if the json
        # stays the same (postgres comparison wise), the object is the same. Otherwise, we got
        # a different object.
        # This is problematic as either the db will grow endlessly or objects will be deleted
        # while still being observed (i.e. the details view).
        deserialized_metadata = FullMetadataSerializer(data=video_metadata)
        deserialized_metadata.is_valid(raise_exception=True)
        try:
             Metadata.objects.get(complete_json=video_metadata)
             continue
        except ObjectDoesNotExist:
            deserialized_metadata.save()

    fetch_metadata = FetchMetadata.load()
    fetch_metadata.data_expires_at = timezone.now() + timedelta(minutes=5)
    if (expires_header := response.headers.get("expires")) is not None:
        fetch_metadata.data_expires_at = timezone.make_aware(
            datetime.strptime(expires_header, "%a, %d %b %Y %H:%M:%S GMT"),
            timezone.utc)
    fetch_metadata.save()


@shared_task
def check_fetch_store_metadata() -> None:
    fetch_metadata = FetchMetadata.load()

    if not fetch_metadata.data_expires_at or fetch_metadata.data_expires_at < timezone.now():
        _update_metadata()
