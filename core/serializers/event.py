from rest_framework import serializers

from core.models import Event



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'group', 'name', 'description', 'event_date', 'event_location']


class EventRequestSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    event_date = serializers.DateTimeField(required=False)
    event_location = serializers.CharField(required=False)



class EventRequestforPatchSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    event_date = serializers.DateTimeField() #?
    event_location = serializers.CharField()