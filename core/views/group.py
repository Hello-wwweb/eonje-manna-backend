from enum import member

from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import MeetingGroup, Member, Membership
from core.serializers.group_member import GroupMemberSerializer
from core.serializers.meeting_group import MeetingGroupSerializer, MeetingGroupRequestSerializer
from drf_yasg.utils import swagger_auto_schema

from core.serializers.membership import MembershipSerializer


class MeetingGroupListView(APIView):
    @swagger_auto_schema(
        responses={
            200: MeetingGroupSerializer(many=True),
        },
    )
    def get(self, request):
        user = request.user
        user_member = Member.objects.get(user = user)
        meeting_groups = MeetingGroup.objects.filter(membership__member=user_member) # 만든 사람이 아니라, 속한 그룹을 가져와야
        serializer = MeetingGroupSerializer(meeting_groups, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=MeetingGroupRequestSerializer,
        responses={
            201: MeetingGroupSerializer(),
            400: "Bad Request",
            500: "internal server error"
        },
    )
    def post(self, request):
        user = request.user

        user_member = Member.objects.get(user=user)
        group_serializer = MeetingGroupSerializer(data=request.data)
        if group_serializer.is_valid():
            with transaction.atomic():
                group_serializer.save(created_by=user)

                membership_serializer = MembershipSerializer(data={
                    'member': user_member.id,
                    'group': group_serializer.instance.id,
                    'nickname': user_member.name
                })
                if membership_serializer.is_valid():
                    membership_serializer.save()
                else:
                    raise membership_serializer.ValidationError(membership_serializer.errors)
            return Response(group_serializer.data, status=status.HTTP_201_CREATED)

        return Response(group_serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class MeetingGroupDetailView(APIView):
    def get_object(self, pk):
        try:
            obj = MeetingGroup.objects.get(pk=pk)
            return obj
        except MeetingGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        responses={
            200: MeetingGroupSerializer(),
            403: "You are not in this group",
            404: "Meeting Group not found",
        },
    )
    def get(self, request, pk):  #authenticate 필요
        obj = self.get_object(pk)

        #authenticate
        user = request.user
        user_member = Member.objects.get(user=user)
        if not Membership.objects.filter(group =obj, member= user_member).exists():
            return Response({"error": "You are not in this group"}, status= status.HTTP_403_FORBIDDEN)

        serializer = MeetingGroupSerializer(obj)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=MeetingGroupSerializer,
        responses={
            200: MeetingGroupSerializer(),
            404: "Meeting Group not found",
            403: "No Permission to Modify",
            400: "Bad Request",
        },
    )
    def put(self, request, pk):
        obj = self.get_object(pk)

        # authenticate
        user = request.user
        if not obj.created_by == user:
            return Response({"error": "No permission to modify"}, status= status.HTTP_403_FORBIDDEN)

        serializer = MeetingGroupSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        responses={
            204: "No Content",
            403: "No Permission to Modify",
            404: "Meeting Group not found",
        },
    )
    def delete(self, request, pk):
        obj = self.get_object(pk)

        # authenticate
        user = request.user
        if not obj.created_by == user:
            return Response({"error": "No permission to modify"}, status=status.HTTP_403_FORBIDDEN)

        obj.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupMemberListView(APIView):
    def get_group(self, group_id: int):
        try:
            return MeetingGroup.objects.get(id=group_id)
        except (MeetingGroup.DoesNotExist, MeetingGroup.MultipleObjectsReturned):
            return None

    def get(self, request, group_id: int):
        group = self.get_group(group_id)
        if group is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        members = Membership.objects.filter(group=group)
        serializer = GroupMemberSerializer(members, many=True)
        return Response(serializer.data)