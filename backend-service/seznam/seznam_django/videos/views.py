from django.views import generic

from .models import Video
from .lib import api_fetch


class IndexView(generic.ListView):
    model = Video
    template_name = "videos/index.html"

    def get(self, request, *args, **kwargs):
        metadata = api_fetch.fetch_videos_metadata()
        api_fetch.store_videos_metadata(metadata)
        return super().get(request, *args, **kwargs)
