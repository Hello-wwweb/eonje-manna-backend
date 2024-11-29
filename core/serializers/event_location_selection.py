from rest_framework import serializers

from core.models import EventLocationSelection


class EventLocationSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventLocationSelection
        fields = [
            "id",
            "member",
            "event",
            "selected_places",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        return EventLocationSelection.objects.create(**validated_data)
