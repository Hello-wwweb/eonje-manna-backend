from rest_framework import serializers


class GroupMemberSerializer(serializers.Serializer):
    name = serializers.CharField(source='member.name')
    nickname = serializers.CharField()
    email = serializers.CharField(source='member.email')
    joined_at = serializers.DateTimeField()

