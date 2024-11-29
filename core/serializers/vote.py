from rest_framework import serializers

from core.models import Vote

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['member', 'event', 'voted_places']


class VoteRequestSerializer(serializers.Serializer):
    event = serializers.IntegerField()
    voted_places = serializers.CharField()