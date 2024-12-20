from rest_framework import serializers

from core.models import MeetingGroup

class MeetingGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingGroup
        fields = ['id', 'name', 'description']


class MeetingGroupRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
