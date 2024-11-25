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
            child=serializers.TimeField(format="%H:%M"),
            allow_empty=False,
        ),
        required=True,
        help_text="가능한 날짜 (YYYY-MM-DD)와 해당 날짜의 가능한 시간 리스트 (HH:MM)"
    )

    def validate_selected_dates(self, value):
        """
        Validate that keys are valid dates and values are valid time lists in HH:MM format.
        """
        for date, times in value.items():
            # Validate date format
            try:
                datetime.strptime(date, "%Y-%m-%d")
            except ValueError:
                raise serializers.ValidationError(
                    f"Invalid date format: {date}. Expected format: YYYY-MM-DD"
                )

            # Validate time list
            for time in times:
                try:
                    datetime.strptime(time, "%H:%M")
                except ValueError:
                    raise serializers.ValidationError(
                        f"Invalid time format: {time} in date {date}. Expected format: HH:MM"
                    )
        return value
