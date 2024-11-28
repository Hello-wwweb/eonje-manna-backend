from rest_framework import serializers
from core.models.marker import Marker


class MarkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marker
        fields = [
            "id",
            "group_id",
            "member_id",
            "latitude",
            "longitude",
            "address",
            "created_at",
        ]
