from functools import reduce
import json
import operator
from typing import Any, Dict

from django.db.models import Q
from django.views import generic

from .models import Drm, Feature, Metadata
from .tasks import check_fetch_store_metadata


class IndexView(generic.ListView):
    template_name = "videos/index.html"

    def get_queryset(self):
        # I suppose this should be somehow handled with Django forms.
        order_string = self.request.GET.get("order", "asc")
        order_prefix = "" if order_string == "asc" else "-"
        order_by = self.request.GET.get("order_by", "name")
        is_featured = self.request.GET.get("is_featured", None)

        drms = [drm.removeprefix("filter_drm_")
                for drm in self.request.GET.keys() if drm.startswith("filter_drm_")]
        features = [feature.removeprefix("filter_feature_")
                    for feature in self.request.GET.keys() if feature.startswith("filter_feature_")]

        is_featured_q = Q(is_featured=True) if is_featured is not None else ~Q(pk__in=[])

        json_search = self.request.GET.get("json_search", None)
        json_search_q = ~Q(pk__in=[])
        if json_search := self.request.GET.get("json_search", None):
            try:
                json_search_q = Q(**{
                    f"complete_json__{json_search.split('=')[0]}": json.loads('{"key":' + json_search.split("=")[1] + '}')["key"]})
            except json.JSONDecodeError:
                raise Exception(f"The query '{json_search}' was not correct.")

        result = Metadata.objects.all().filter(is_featured_q & json_search_q)
        for drm in drms:
            result = result.filter(drms__name=drm)
        for feature in features:
            result = result.filter(features__name=feature)
        return result.distinct().order_by(f"{order_prefix}{order_by}")

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context_data = super().get_context_data(**kwargs)
        context_data["all_drms"] = [data[0] for data in Drm.objects.values_list("name")]
        context_data["all_features"] = [data[0] for data in Feature.objects.values_list("name")]
        return context_data

    def get(self, request, *args, **kwargs):
        check_fetch_store_metadata()
        return super().get(request, *args, **kwargs)


class DetailView(generic.DetailView):
    model = Metadata
    template_name = "videos/detail.html"
