from django.urls import path

from videos import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("api/", views.ApiMetadataViewSet.as_view({ "get": "list" }), name="metadata"),
    path("api/<int:pk>/", views.ApiFullMetadataViewSet.as_view({ "get": "retrieve" }), name="metadata-detail"),
    path("api/drm/", views.ApiDrmViewSet.as_view({ "get": "list" }), name="drm"),
    path("api/drm/<int:pk>/", views.ApiDrmViewSet.as_view({ "get": "retrieve" }), name="drm-detail"),
    path("api/feature/", views.ApiFeatureViewSet.as_view({ "get": "list" }), name="feature"),
    path("api/feature/<int:pk>/", views.ApiFeatureViewSet.as_view({ "get": "retrieve" }), name="feature-detail"),
]
