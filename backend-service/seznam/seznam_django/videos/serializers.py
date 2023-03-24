from rest_framework import serializers

from videos.models import Drm, Feature, Metadata


class DrmSerializer(serializers.HyperlinkedModelSerializer):
    # Unique on model leads to failing validation during deserialization, which is stupid.
    name = serializers.CharField(validators=[])

    class Meta:
        model = Drm
        exclude = []

    def to_internal_value(self, data):
        return super().to_internal_value({ "name": data })


class FeatureSerializer(serializers.HyperlinkedModelSerializer):
    # Unique on model leads to failing validation during deserialization, which is stupid.
    name = serializers.CharField(validators=[])

    class Meta:
        model = Feature
        exclude = []

    def to_internal_value(self, data):
        return super().to_internal_value({ "name": data })


class FullMetadataSerializer(serializers.HyperlinkedModelSerializer):
    short_name = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    features = FeatureSerializer(many=True)
    drms = DrmSerializer(many=True)

    class Meta:
        model = Metadata
        exclude = []

    def to_internal_value(self, data):
        # Some fields in the input JSON have non-Pythonic names; they are renamed here.
        data_update = {
            "short_name": data["shortName"],
            "icon_uri": data["iconUri"],
            "manifest_uri": data["manifestUri"],
            "is_featured": data["isFeatured"],
            "description": data["description"] or "",
            "features": data["features"],
            "drms": data["drm"],
            "complete_json": data,
        }
        return super().to_internal_value(data | data_update)

    def create(self, validated_data):
        features = (Feature.objects.get_or_create(**feature)[0] for feature in validated_data.pop("features"))
        drms = (Drm.objects.get_or_create(**drm)[0] for drm in validated_data.pop("drms"))
        metadata = Metadata.objects.create(**validated_data)
        if features:
            metadata.features.set(features)
        if drms:
            metadata.drms.set(drms)
        metadata.save()
        return metadata


class MetadataSerializer(FullMetadataSerializer):
    class Meta:
        model = Metadata
        fields = ["id", "url", "name", "features", "drms", "short_name", "is_featured"]