from django.views import generic

from .models import Video


class IndexView(generic.ListView):
    model = Video
    template_name = "videos/index.html"

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
