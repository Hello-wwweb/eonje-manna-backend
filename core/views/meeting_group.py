from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import MeetingGroup
from core.serializers.meeting_group import MeetingGroupSerializer, MeetingGroupRequestSerializer
from drf_yasg.utils import swagger_auto_schema

class MeetingGroupListView(APIView):
    @swagger_auto_schema(
        responses={
            200: MeetingGroupSerializer(many=True),
        },
    )
    def get(self, request):
        user = request.user
        meeting_groups = MeetingGroup.objects.filter(created_by=user)
        serializer = MeetingGroupSerializer(meeting_groups, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=MeetingGroupRequestSerializer,
        responses={
            201: MeetingGroupSerializer(),
            400: "Bad Request",
        },
    )
    def post(self, request):
        user = request.user
        serializer = MeetingGroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
            404: "Meeting Group not found",
        },
    )
    def get(self, request, pk):
        obj = self.get_object(pk)
        serializer = MeetingGroupSerializer(obj)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=MeetingGroupSerializer,
        responses={
            200: MeetingGroupSerializer(),
            404: "Meeting Group not found",
            400: "Bad Request",
        },
    )
    def put(self, request, pk):
        obj = self.get_object(pk)
        serializer = MeetingGroupSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        responses={
            204: "No Content",
            404: "Meeting Group not found",
        },
    )
    def delete(self, request, pk):
        obj = self.get_object(pk)
        obj.delete()