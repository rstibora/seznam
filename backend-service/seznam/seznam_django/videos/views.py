from typing import Any, Dict, Sequence

from django.views import generic

from .models import Metadata
from .tasks import fetch_and_store_metadata


class IndexView(generic.ListView):
    model = Metadata
    template_name = "videos/index.html"

    def get_ordering(self) -> Sequence[str]:
        order_string = self.request.GET.get("order", "asc")
        order_prefix = "" if order_string == "asc" else "-"

        order_by = self.request.GET.get("order_by", "name")
        return [f"{order_prefix}{order_by}"]

    def get(self, request, *args, **kwargs):
        fetch_and_store_metadata()
        return super().get(request, *args, **kwargs)
