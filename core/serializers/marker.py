from rest_framework import serializers
from core.models.marker import Marker


class MarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marker
        fields = [
            "id",
            "event_id",
            "member_id",
            "latitude",
            "longitude",
            "place_name",
            "created_at",
        ]
