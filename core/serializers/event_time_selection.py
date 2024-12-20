from rest_framework import serializers
from core.models import EventDateSelection
from datetime import datetime


class EventDateSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDateSelection
        fields = ['member', 'event', 'selected_dates']


class EventDateSelectionRequestSerializer(serializers.Serializer):
    event = serializers.IntegerField(
        required=True,
        help_text="이벤트의 ID (정수 값)"
    )
    selected_dates = serializers.DictField(
        child=serializers.ListField(
            child=serializers.CharField(),
            allow_empty=False,
        ),
        required=True,
        help_text="가능한 날짜 (YYYY-MM-DD)와 해당 날짜의 가능한 시간 리스트 (HH:MM)"
    )

    