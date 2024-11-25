from core.models.member import Member
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.models import EventDateSelection
from core.serializers.event_time_selection import EventDateSelectionRequestSerializer, EventDateSelectionSerializer

class EventDateSelectionView(APIView):
    @swagger_auto_schema(
        request_body=EventDateSelectionRequestSerializer,  # 요청 본문을 설명
        responses={
            201: EventDateSelectionSerializer,  # 성공 응답 정의
            400: "Invalid input"               # 실패 응답 정의
        },
        operation_summary="Create Event Date Selection",
        operation_description="Creates a new EventDateSelection object with the provided member, event, and selected dates."
    )
    def post(self, request):
        serializer = EventDateSelectionRequestSerializer(data=request.data)
        user = request.user
    
        # request.user와 연결된 Member 객체 가져오기
        try:
            member = Member.objects.get(user=user)
        except Member.DoesNotExist:
            return Response(
                {"error": "Member not found for the current user."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if serializer.is_valid():
            validated_data = serializer.validated_data
            event_id = validated_data['event']
            selected_dates = validated_data['selected_dates']
            
            # EventDateSelection 저장
            event_date_selection = EventDateSelection.objects.create(
                member=member,
                event_id=event_id,
                selected_dates=selected_dates
            )

            response_serializer = EventDateSelectionSerializer(event_date_selection)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDateSelectionResultView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('event', openapi.IN_QUERY, description="Event ID", type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('date', openapi.IN_QUERY, description="Date in YYYY-MM-DD format", type=openapi.TYPE_STRING, required=True),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "event": openapi.Schema(type=openapi.TYPE_INTEGER, description="Event ID"),
                    "date": openapi.Schema(type=openapi.TYPE_STRING, description="Date"),
                    "intersecting_times": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description="List of intersecting times")
                }
            ),
            400: "Invalid input",
            200: "No records found"
        },
        operation_summary="Get Intersecting Times",
        operation_description="Retrieves the intersecting times for a given event and date based on all members' availability."
    )
    def get(self, request):
        event_id = request.query_params.get("event")
        date_to_search = request.query_params.get("date")

        if not event_id or not date_to_search:
            return Response({"error": "Missing 'event' or 'date' parameter."}, status=400)
        
        event_records = EventDateSelection.objects.filter(event=event_id)

        if not event_records.exists():
            return Response({"message": f"No records found for event {event_id}"}, status=200)
        
        intersecting_times = None
        for record in event_records:
            selected_dates = record.selected_dates
            if date_to_search in selected_dates:
                current_times = set(selected_dates[date_to_search])
                if intersecting_times is None:
                    intersecting_times = current_times
                else:
                    intersecting_times = intersecting_times.intersection(current_times)

        if not intersecting_times:
            return Response({
                "event": event_id,
                "date": date_to_search,
                "intersecting_times": []
            }, status=200)

        return Response({
            "event": event_id,
            "date": date_to_search,
            "intersecting_times": sorted(intersecting_times)
        }, status=200)


class EventDateSelectionAllView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('event', openapi.IN_QUERY, description="Event ID", type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('date', openapi.IN_QUERY, description="Date in YYYY-MM-DD format", type=openapi.TYPE_STRING, required=True),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "member_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Member ID"),
                        "member_name": openapi.Schema(type=openapi.TYPE_STRING, description="Member Name"),
                        "available_times": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING), description="List of available times"),
                    }
                )
            ),
            404: "Member not found",
            400: "Invalid input"
        },
        operation_summary="Get All Members' Availability",
        operation_description="Retrieves the availability of all members for a specific event and date, with the requesting user's data at the top."
    )
    def get(self, request):
        user = request.user
        try:
            request_member = Member.objects.get(user=user)
        except Member.DoesNotExist:
            return Response(
                {"error": "Member not found for the current user."},
                status=status.HTTP_404_NOT_FOUND
            )
        event_id = request.query_params.get("event")
        date_to_search = request.query_params.get("date")

        if not event_id or not date_to_search:
            return Response({"error": "Missing 'event' or 'date' parameter."}, status=400)

        records = EventDateSelection.objects.filter(
            event=event_id,
            selected_dates__has_key=date_to_search
        )

        request_member_info = None
        members = []

        for record in records:
            member = record.member
            selected_dates = record.selected_dates
            available_times = selected_dates.get(date_to_search, [])

            member_info = {
                "member_id": member.id,
                "member_name": member.name,
                "available_times": available_times
            }

            if member == request_member:
                request_member_info = member_info
            else:
                members.append(member_info)

        if request_member_info:
            result = [request_member_info] + members
        else:
            result = members

        return Response(result, status=200)
