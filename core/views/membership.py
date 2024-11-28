from enum import member

from django.db import IntegrityError
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import MeetingGroup, Member, Membership
from core.serializers.meeting_group import MeetingGroupSerializer
from drf_yasg.utils import swagger_auto_schema

from core.serializers.membership import MembershipSerializer, MembershipInviteSerializer, MembershipNicknameSerializer

class MembershipListView(APIView):
    def post(self, request, group_id: int, *args, **kwargs):
        serializer = MembershipInviteSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')

            try:
                member = Member.objects.get(email=email)
            except Member.DoesNotExist:
                return Response({"detail": "Member not found."}, status=status.HTTP_404_NOT_FOUND)

            try:
                group = MeetingGroup.objects.get(id=group_id)
            except MeetingGroup.DoesNotExist:
                return Response({"detail": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

            try:
                membership = Membership.objects.create(
                    member=member,
                    group=group,
                    nickname=member.name
                )

            except IntegrityError:
                return Response({"detail": "Member is already a member of this group."},
                                status=status.HTTP_400_BAD_REQUEST)

            return Response(MembershipSerializer(membership).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MembershipDetailView(APIView):
    def get_group(self, pk):
        try:
            obj = MeetingGroup.objects.get(pk=pk)
            return obj
        except MeetingGroup.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        responses={
            200: MembershipSerializer(many = True),
            403: "You are not in this group",
            404: "Meeting Group not found",
        },
    )
    def get(self, request, pk):  # authenticate 필요
        obj = self.get_group(pk)

        # authenticate
        user = request.user
        user_member = Member.objects.get(user=user)
        if not Membership.objects.filter(group=obj, member=user_member).exists():
            return Response({"error": "You are not in this group"}, status=status.HTTP_403_FORBIDDEN)

        memberships = Membership.objects.filter(group =obj)
        serializer = MembershipSerializer(memberships, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=MembershipInviteSerializer,
        responses={
            200: MembershipSerializer(),
            404: "Not Found",
            403: "You ar not in this group",
            400: "Bad Request",
        },
    )
    def post(self, request, pk):
        obj = self.get_group(pk)

        # authenticate
        user = request.user
        user_member = Member.objects.get(user=user)
        if not Membership.objects.filter(group=obj, member=user_member).exists():
            return Response({"error": "You are not in this group"}, status=status.HTTP_403_FORBIDDEN)

        #member를 email로 찾기
        try:
            invited_member = Member.objects.get(email = request.data.get("email"))
        except Member.DoesNotExist:
            return Response({"error": "Member with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

        #member가 이미 존재하는지
        if Membership.objects.filter( group=obj, member=invited_member).exists():
            return Response({"error": "This member is already in the group"}, status=status.HTTP_400_BAD_REQUEST)

        #멤버 추가
        serializer = MembershipSerializer(data= {
            "member" :invited_member.id,
            "group": obj.id,
            "nickname" : invited_member.name})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=MembershipNicknameSerializer,
        responses={
            200: MembershipSerializer(),
            404: "Not Found",
            403: "You ar not in this group",
            400: "Bad Request",
        },
    )
    def put(self, request, pk):
        obj = self.get_group(pk)

        # authenticate
        user = request.user
        user_member = Member.objects.get(user=user)
        if not Membership.objects.filter(group=obj, member=user_member).exists():
            return Response({"error": "You are not in this group"}, status=status.HTTP_403_FORBIDDEN)

        # 닉넴 변경
        user_membership = Membership.objects.get(member = user_member)
        serializer = MembershipSerializer(user_membership,  data= request.data, partial = True)
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
    def delete(self, request, pk):  ##방장에게 강퇴기능 추가해야?
        obj = self.get_group(pk)

        user = request.user
        user_member = Member.objects.get(user=user)
        # 방장 탈퇴 막기
        if  obj.created_by == user:
            return Response({"error": "You are admin! cannot exit"}, status=status.HTTP_403_FORBIDDEN)

        user_membership = Membership.objects.get(member = user_member)
        user_membership.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)