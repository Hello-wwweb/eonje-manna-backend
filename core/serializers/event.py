from rest_framework import serializers

from core.models import Event



class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'group', 'name', 'description', 'event_date', 'event_location']


class EventRequestforPostSerializer(serializers.Serializer):

    name = serializers.CharField()
    description = serializers.CharField()



class EventRequestforPatchSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    event_date = serializers.DateTimeField() #?
    event_location = serializers.CharField()