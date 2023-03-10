from typing import Any, Dict, Sequence

from django.views import generic

from .models import Video


class IndexView(generic.ListView):
    model = Video
    template_name = "videos/index.html"

    def get_ordering(self) -> Sequence[str]:
        order_string = self.request.GET.get("order", "asc")
        order_prefix = "" if order_string == "asc" else "-"

        order_by = self.request.GET.get("order_by", "name")
        return [f"{order_prefix}{order_by}"]
