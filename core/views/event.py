from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.models import Event, MeetingGroup
from core.serializers.event import EventSerializer, \
    EventRequestforPatchSerializer, EventRequestSerializer

from drf_yasg.utils import swagger_auto_schema
class MyEventListView(APIView):
    @swagger_auto_schema(
        responses={
            200: EventSerializer(many=True),
        },
    )
    def get(self, request):
        user_member = Member.objects.get(user = request.user)
        try:
            groups = Membership.objects.filter(member=user_member).values_list('group', flat=True)
        except (MeetingGroup.DoesNotExist, MeetingGroup.MultipleObjectsReturned):
            return Response(status=status.HTTP_404_NOT_FOUND)

        events = Event.objects.filter(group__in=groups).order_by('event_date')
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

class EventListView(APIView):
    @swagger_auto_schema(
        responses={
            200: EventSerializer(many=True),
        },
    )
    def get(self, request, group_id: int):
        try:
            group = MeetingGroup.objects.get(id=group_id)
        except (MeetingGroup.DoesNotExist, MeetingGroup.MultipleObjectsReturned):
            return Response(status=status.HTTP_404_NOT_FOUND)

        events = Event.objects.filter(group=group)
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=EventRequestSerializer,
        responses={
            201: EventSerializer(),
            400: "Bad Request",
            404: "Group not found",
        },
    )
    def post(self, request, group_id: int):
        user = request.user

        try:
            group = MeetingGroup.objects.get(id=group_id)
        except (MeetingGroup.DoesNotExist, MeetingGroup.MultipleObjectsReturned):
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = EventRequestSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            description = serializer.validated_data.get('description')
            event_date = serializer.validated_data.get('event_date', None)
            event_location = serializer.validated_data.get('event_location', None)

            event = Event.objects.create(
                name=name,
                description=description,
                group=group,
                created_by=user,
                event_date=event_date,
                event_location=event_location
            )

            return Response(EventSerializer(event).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventDetailView(APIView):
    def get_object(self, pk):
        try:
            obj = Event.objects.get(pk=pk)
            return obj
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        responses={
            200: EventSerializer(),
            404: "Event not found",
        },
    )
    def get(self, request, pk):
        obj = self.get_object(pk)
        serializer = EventSerializer(obj)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=EventRequestforPatchSerializer,
        responses={
            200: EventSerializer(),
            404: "Event not found",
            400: "Bad Request",
        },
    )
    def patch(self, request, pk):
        obj = self.get_object(pk)
        serializer = EventSerializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        responses={
            204: "No Content",
            404: "Event not found",
        },
    )
    def delete(self, request, pk):
        obj = self.get_object(pk)

        # authenticate
        if not request.user == obj.created_by:
            return Response({"error": "Permission Denied"}, status=status.HTTP_403_FORBIDDEN)

        obj.delete()
# ##
# def create_event(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)
#             event = Event.objects.create(
#                 group_id=data.get("group_id"),
#                 name=data.get("name"),
#                 description=data.get("description"),
#                 created_by_id=data.get("created_by_id"),
#             )
#             return JsonResponse({"message": "Event create successful", "event_id": event.id}, status=201)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)
#     return HttpResponse(status=405)
#
#
# def update_event(request, event_id):
#     if request.method == "PUT":
#         try:
#             user = request.user
#             data = json.loads(request.body)
#             event = get_object_or_404(Event, id=event_id)
#
#             #authenticate
#             if not Member.objects.filter(group = event.group, user=user).exists():
#                 return JsonResponse({"error": "Permission Denied"},status = 403)
#
#             event.name = data.get("name", event.name)
#             event.description = data.get("description", event.description)
#             event.event_date = data.get("event_date", event.event_date)
#             event.event_location = data.get("event_location", event.event_location)
#             event.save()
#             return JsonResponse({"message": "Event update successful"}, status=200)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)
#     return HttpResponse(status=405)
#
#
# def delete_event(request, event_id):
#     if request.method == "DELETE":
#         try:
#             user = request.user
#             event = get_object_or_404(Event, id=event_id)
#
#             # authenticate
#             if not Member.objects.filter(group=event.group, user=user).exists():
#                 return JsonResponse({"error": "Permission Denied"}, status=403)
#
#
#             event.delete()
#             return JsonResponse({"message": "Event deleted"}, status=200)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)
#     return HttpResponse(status=405)
#
# def retrieve_event(request, event_id):
#     if request.method == "GET":
#         try:
#             user = request.user
#             event = get_object_or_404(Event, id=event_id)
#
#             # authenticate
#             if not Member.objects.filter(group=event.group, user=user).exists():
#                 return JsonResponse({"error": "Permission Denied"}, status=403)
#
#             event_data = {
#                 "id": event.id,
#                 "group_id": event.group_id,
#                 "name": event.name,
#                 "description": event.description,
#                 "event_date": event.event_date,
#                 "event_location": event.event_location,
#                 "created_by_id": event.created_by_id,
#             }
#             return JsonResponse(event_data, status=200)
#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)
#     return HttpResponse(status=405)


