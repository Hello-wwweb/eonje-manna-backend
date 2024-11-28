from enum import member
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


from core.models import MeetingGroup, Member, Membership
from core.serializers.group_member import GroupMemberSerializer
from core.serializers.meeting_group import MeetingGroupSerializer
from drf_yasg.utils import swagger_auto_schema

from core.serializers.membership import MembershipSerializer, MembershipInviteSerializer, MembershipNicknameSerializer
from core.serializers.profile import ProfileSerializer, ProfileModifySerializer
from core.serializers.signup import SignupSerializer


class MemberListView(APIView):
    @swagger_auto_schema(
        responses={
            200: ProfileSerializer(),
        },
    )
    def get(self, request):
        user = request.user
        try:
            user_member = Member.objects.get(user=user)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProfileSerializer(data={
            "id": user.id,
            "username": user.username,
            "name": user_member.name,
            "email": user_member.email
        })

        if serializer.is_valid():
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=ProfileModifySerializer,
        responses={
            200: ProfileSerializer(),
            400: "Bad Request",
            404: "Group not found",
        },
    )
    def patch(self, request):
        serializer = ProfileModifySerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        user_member = Member.objects.get(user = user)
        # 기존 거랑 같은지
        old_password = serializer.validated_data.get('old_password')
        if not check_password(old_password, user.password):
            return Response({"error": "Old password is incorrect"}, status=status.HTTP_403_FORBIDDEN)

        # 변경
        if 'name' in serializer.validated_data:
            user_member.name = serializer.validated_data['name']
        if 'email' in serializer.validated_data:
            user_member.email = serializer.validated_data['email']
        if 'new_password' in serializer.validated_data:
            user.set_password(serializer.validated_data['new_password'])

        user_member.save()
        user.save()

        return Response({"message": "Profile update Successful"}, status=status.HTTP_200_OK)

