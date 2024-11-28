from rest_framework import serializers

from core.models import MeetingGroup, Membership


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['id', 'member', 'group', 'nickname', 'joined_at' ]


class MembershipInviteSerializer(serializers.Serializer):
    email = serializers.CharField(max_length = 100)

class MembershipNicknameSerializer(serializers.Serializer):
    nickname = serializers.CharField(max_length = 120)