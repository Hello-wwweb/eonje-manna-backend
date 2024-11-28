from rest_framework import serializers

from core.models import MeetingGroup

class MeetingGroupSerializer(serializers.ModelSerializer):
    created_by = serializers.IntegerField(read_only=True)
    class Meta:
        model = MeetingGroup
        fields = ['id', 'name', 'description', 'created_by']


class MeetingGroupRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
