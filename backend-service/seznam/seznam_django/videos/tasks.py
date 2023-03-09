from datetime import datetime, timedelta, timezone

from celery import shared_task
from django.utils import timezone
from pydantic import BaseModel, Field
import requests

from videos.models import Video, FetchMetadata


VIDEOS_URL = ("https://gist.githubusercontent.com/nextsux/f6e0327857c88caedd2dab13affb72c1"
              "/raw/04441487d90a0a05831835413f5942d58026d321/videos.json")


class FetchFailed(Exception):
    pass


class VideoMetadata(BaseModel):
    name: str
    short_name: str = Field(alias="shortName")
    descritption: str = ""


@shared_task
def fetch_and_store_metadata() -> None:
    fetch_metadata = FetchMetadata.load()

    # Data is fresh, no need to fetch.
    if fetch_metadata.data_expires_at and fetch_metadata.data_expires_at > timezone.now():
        return

    response = requests.get(VIDEOS_URL)

    if not response.ok:
        raise FetchFailed("Could not fetch videos metadata.")

    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        raise FetchFailed("Could not parse videos metadata json.")

    video_metadata = (VideoMetadata.parse_obj(video_json) for video_json in response_json)

    Video.objects.all().delete()
    Video.objects.bulk_create([
        Video(
            name=video_metadata.name,
            short_name=video_metadata.short_name,
            description=video_metadata.descritption)
        for video_metadata in video_metadata])

    fetch_metadata.data_expires_at = timezone.now() + timedelta(minutes=5)
    if (expires_header := response.headers.get("expires")) is not None:
        fetch_metadata.data_expires_at = timezone.make_aware(
            datetime.strptime(expires_header, "%a, %d %b %Y %H:%M:%S GMT"),
            timezone.utc)
    fetch_metadata.save()
