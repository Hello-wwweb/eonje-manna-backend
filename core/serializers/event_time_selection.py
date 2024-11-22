from rest_framework import serializers
from core.models import EventDateSelection

class EventDateSelectionSerializer(serializers.ModelSerializer):
    #들어가야하는 정보: member, event, selected_dates
    class Meta:
        model = EventDateSelection
        fields = ['member', 'event', 'selected_dates']
        


class EventDateSelectionRequestSerializer(serializers.Serializer):
    event = serializers.IntegerField(
        required=True,
        help_text="이벤트의 ID (정수 값)"
    )
    selected_dates = serializers.ListField(
        child=serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S"),
        required=True,
        allow_empty=False,
        help_text="Datetime 값을 문자열로 저장할 리스트"
    )
