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
    short_name: str = Field(alias="shortName", default="")
    icon_uri: str = Field(alias="iconUri", default="")
    manifest_uri: str = Field(alias="manifestUri", default="")
    descritption: str = ""
    is_featured: bool = Field(alias="isFeatured")
    drm: list[str]
    features: list[str]


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

    video_metadata_models_and_jsons = [(MetadataModel.parse_obj(video_json), video_json)
                                       for video_json in response_json]

    for video_metadata, complete_json in video_metadata_models_and_jsons:
        # Since there is not unique identifier in the json, it is assumed that if the json
        # stays the same (postgres comparison wise), the object is the same. Otherwise, we got
        # different object.
        # This is problematic as either the db will grow endlessly or objects will be deleted udner
        # while still being observed (e.g. the details view).
        try:
            Metadata.objects.get(complete_json=complete_json)
            continue
        except ObjectDoesNotExist:
            features = (Feature.objects.get_or_create(name=feature)[0] for feature in video_metadata.features)
            drms = (Drm.objects.get_or_create(name=drm)[0] for drm in video_metadata.drm)
            metadata = Metadata.objects.create(
                name=video_metadata.name,
                short_name=video_metadata.short_name,
                icon_uri=video_metadata.icon_uri,
                manifest_uri=video_metadata.manifest_uri,
                description=video_metadata.descritption,
                is_featured=video_metadata.is_featured,
                complete_json=complete_json)
            if features:
                metadata.features.set(features)
            if drms:
                metadata.drms.set(drms)
            metadata.save()

    fetch_metadata.data_expires_at = timezone.now() + timedelta(minutes=5)
    if (expires_header := response.headers.get("expires")) is not None:
        fetch_metadata.data_expires_at = timezone.make_aware(
            datetime.strptime(expires_header, "%a, %d %b %Y %H:%M:%S GMT"),
            timezone.utc)
    fetch_metadata.save()
