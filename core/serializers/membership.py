from rest_framework import serializers

from core.models import MeetingGroup, Membership


class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['id', 'member', 'group', 'nickname', 'joined_at' ]