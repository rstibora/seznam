from datetime import datetime, timedelta, timezone

from celery import shared_task
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from pydantic import BaseModel, Field
import requests

from videos.models import Drm, Feature, FetchMetadata, Metadata


VIDEOS_URL = ("https://gist.githubusercontent.com/nextsux/f6e0327857c88caedd2dab13affb72c1"
              "/raw/04441487d90a0a05831835413f5942d58026d321/videos.json")


class FetchFailed(Exception):
    pass


class MetadataModel(BaseModel):
    name: str
    short_name: str = Field(alias="shortName")
    icon_uri: str = Field(alias="iconUri")
    manifest_uri: str = Field(alias="manifestUri")
    description: str | None  = None
    is_featured: bool = Field(alias="isFeatured")
    drm: list[str]
    features: list[str]


def _update_metadata() -> None:
    response = requests.get(VIDEOS_URL)

    if not response.ok:
        raise FetchFailed("Could not fetch videos metadata.")

    response_json = response.json()
    video_metadata_models_and_jsons = [(MetadataModel.parse_obj(video_json), video_json)
                                        for video_json in response_json]


    for video_metadata, complete_json in video_metadata_models_and_jsons:
        # Since there is no unique identifier in the json, it is assumed that if the json
        # stays the same (postgres comparison wise), the object is the same. Otherwise, we got
        # a different object.
        # This is problematic as either the db will grow endlessly or objects will be deleted
        # while still being observed (i.e. the details view).
        try:
            Metadata.objects.get(complete_json=complete_json)
            continue
        except ObjectDoesNotExist:
            features = (Feature.objects.get_or_create(name=feature)[0] for feature in video_metadata.features)
            drms = (Drm.objects.get_or_create(name=drm)[0] for drm in video_metadata.drm)
            metadata = Metadata.objects.create(
                complete_json=complete_json, **video_metadata.dict(exclude={"drm", "features"}))

            if features:
                metadata.features.set(features)
            if drms:
                metadata.drms.set(drms)
            metadata.save()

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
