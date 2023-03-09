from collections.abc import Iterable

from pydantic import BaseModel, Field
import requests

from ..models import Video


VIDEOS_URL = ("https://gist.githubusercontent.com/nextsux/f6e0327857c88caedd2dab13affb72c1"
              "/raw/04441487d90a0a05831835413f5942d58026d321/videos.json")


class FetchFailed(Exception):
    pass


class VideoMetadata(BaseModel):
    name: str
    short_name: str = Field(alias="shortName")
    descritption: str = ""


def fetch_videos_metadata() -> Iterable[VideoMetadata]:
    response = requests.get(VIDEOS_URL)

    if not response.ok:
        raise FetchFailed("Could not fetch videos metadata.")

    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        raise FetchFailed("Could not parse videos metadata json.")

    return (VideoMetadata.parse_obj(video_json) for video_json in response_json)


def store_videos_metadata(metadata: Iterable[VideoMetadata]) -> None:
    Video.objects.all().delete()
    Video.objects.bulk_create([
        Video(
            name=video_metadata.name,
            short_name=video_metadata.short_name,
            description=video_metadata.descritption)
        for video_metadata in metadata])
