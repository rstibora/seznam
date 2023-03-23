from videos.models import Drm, Feature, Metadata

from rest_framework import serializers



class DrmSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Drm
        exclude = []


class FeatureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Feature
        exclude = []


class MetadataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Metadata
        fields = ["url", "name", "features", "drms"]


class FullMetadataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Metadata
        exclude = []
