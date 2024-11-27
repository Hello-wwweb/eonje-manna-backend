from rest_framework import serializers


class GroupMemberSerializer(serializers.Serializer):
    username = serializers.CharField(source='member.user.username')
    user_id = serializers.IntegerField(source='member.user.id')
    name = serializers.CharField(source='member.name')
    nickname = serializers.CharField()
    email = serializers.CharField(source='member.email')
    joined_at = serializers.DateTimeField()

