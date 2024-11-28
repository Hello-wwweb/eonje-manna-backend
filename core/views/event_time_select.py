from collections import defaultdict
from datetime import datetime
from xml.dom import ValidationErr

from django.db import IntegrityError

from core.models.member import Member
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.models import EventDateSelection
from core.serializers.event_time_selection import EventDateSelectionRequestSerializer, EventDateSelectionSerializer

class EventDateSelectionUserView(APIView):
    def get(self, request, event_id, *args, **kwargs):
        if


class EventDateSelectionView(APIView):
    @swagger_auto_schema(
    request_body=EventDateSelectionRequestSerializer,
    responses={
        201: EventDateSelectionSerializer,
        400: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "error": openapi.Schema(type=openapi.TYPE_STRING, description="Error message")
            }
        )
    },
    operation_summary="Create Event Date Selection",
    operation_description="Creates a new EventDateSelection object with the provided member, event, and selected dates."
)
    def post(self, request):
        serializer = EventDateSelectionRequestSerializer(data=request.data)
        user = request.user

        # Member 객체 가져오기
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

            try:
                # EventDateSelection 저장
                event_date_selection = EventDateSelection.objects.create(
                    member=member,
                    event_id=event_id,
                    selected_dates=selected_dates
                )

                response_serializer = EventDateSelectionSerializer(event_date_selection)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)

            except IntegrityError as e:
                # Catching the IntegrityError (unique constraint violation)
                return Response(
                    {
                        "error": "A selection for this event already exists for the current member.",
                        "error_code": "unique_constraint_violation"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class EventDateSelectionDetailView(APIView):
        @swagger_auto_schema(
    manual_parameters=[
        openapi.Parameter(
            'pk',
            openapi.IN_PATH,
            description="Primary Key of the EventDateSelection",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    request_body=EventDateSelectionRequestSerializer,
    responses={
        200: EventDateSelectionSerializer,
        403: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "error": openapi.Schema(type=openapi.TYPE_STRING, description="Permission denied")
            }
        ),
        400: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "error": openapi.Schema(type=openapi.TYPE_STRING, description="Invalid input or Event ID mismatch")
            }
        ),
        404: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "error": openapi.Schema(type=openapi.TYPE_STRING, description="Record not found")
            }
        )
    },
    operation_summary="Update Event Date Selection",
    operation_description="Replaces the selected dates for the provided EventDateSelection, removing all existing entries."
)
        def patch(self, request, pk):  # 기존 데이터 삭제 후 새로운 데이터 추가
            try:
                # EventDateSelection 객체를 가져옵니다.
                record = EventDateSelection.objects.get(pk=pk)
            except EventDateSelection.DoesNotExist:
                return Response(
                    {"error": f"EventDateSelection with pk {pk} not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

            user = request.user
            try:
                # 현재 사용자에 해당하는 Member 객체를 가져옵니다.
                request_member = Member.objects.get(user=user)
            except Member.DoesNotExist:
                return Response(
                    {"error": "Member not found for the current user."},
                    status=status.HTTP_404_NOT_FOUND
                )   

            # 권한 검사: 기록의 member와 요청한 member가 일치하는지 확인
            if record.member != request_member:
                return Response(
                    {"error": "You do not have permission to modify this record."},
                    status=status.HTTP_403_FORBIDDEN
                )

            # 요청 데이터 유효성 검사
            serializer = EventDateSelectionRequestSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            validated_data = serializer.validated_data
            date_to_update = validated_data["selected_dates"]
            event_id = validated_data["event"]

            # Event ID 확인
            if event_id != record.event.id:
                return Response(
                    {"error": f"Event ID mismatch. Expected {record.event.id}, got {event_id}."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # 기존 데이터 삭제 및 새로운 데이터 추가
            record.selected_dates.clear()
            for date, times in date_to_update.items():
                record.selected_dates[date] = times

            # 데이터 저장
            record.save()

            # 수정된 데이터를 직렬화하여 반환
            response_serializer = EventDateSelectionSerializer(record)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
   
    

    

    

# class EventDateSelectionResultView(APIView): 
#     @swagger_auto_schema(
#         manual_parameters=[
#             openapi.Parameter('event', openapi.IN_QUERY, description="Event ID", type=openapi.TYPE_INTEGER, required=True),
#             openapi.Parameter('date', openapi.IN_QUERY, description="Date in YYYY-MM-DD format", type=openapi.TYPE_STRING, required=True),
#         ],
#         responses={
#             200: openapi.Schema(
#                 type=openapi.TYPE_OBJECT,
#                 properties={
#                     "event": openapi.Schema(type=openapi.TYPE_INTEGER, description="Event ID"),
#                     "date": openapi.Schema(type=openapi.TYPE_STRING, description="Date"),
#                     "intersecting_times": openapi.Schema(
#                         type=openapi.TYPE_ARRAY,
#                         items=openapi.Items(type=openapi.TYPE_STRING),
#                         description="List of intersecting times"
#                     )
#                 }
#             ),
#             400: openapi.Schema(
#                 type=openapi.TYPE_OBJECT,
#                 properties={
#                     "error": openapi.Schema(type=openapi.TYPE_STRING, description="Invalid input")
#                 }
#             ),
#             404: openapi.Schema(
#                 type=openapi.TYPE_OBJECT,
#                 properties={
#                     "message": openapi.Schema(type=openapi.TYPE_STRING, description="No records found")
#                 }
#             )
#         },
#         operation_summary="Get Intersecting Times",
#         operation_description="Retrieves the intersecting times for a given event and date based on all members' availability."
#     )
#     def get(self, request):
#         event_id = request.query_params.get("event")
#         date_to_search = request.query_params.get("date")

#         if not event_id or not date_to_search:
#             return Response({"error": "Missing 'event' or 'date' parameter."}, status=400)

#         event_records = EventDateSelection.objects.filter(event=event_id)

#         if not event_records.exists():
#             return Response({"message": f"No records found for event {event_id}"}, status=200)

#         intersecting_times = None
#         for record in event_records:
#             selected_dates = record.selected_dates
#             if date_to_search in selected_dates:
#                 current_times = set(selected_dates[date_to_search])
#                 if intersecting_times is None:
#                     intersecting_times = current_times
#                 else:
#                     intersecting_times = intersecting_times.intersection(current_times)

#         if not intersecting_times:
#             return Response({
#                 "event": event_id,
#                 "date": date_to_search,
#                 "intersecting_times": []
#             }, status=200)

#         return Response({
#             "event": event_id,
#             "date": date_to_search,
#             "intersecting_times": sorted(intersecting_times)
#         }, status=200)


# class EventDateSelectionAllView(APIView):
#     @swagger_auto_schema(
#         manual_parameters=[
#             openapi.Parameter('event', openapi.IN_QUERY, description="Event ID", type=openapi.TYPE_INTEGER, required=True),
#             openapi.Parameter('date', openapi.IN_QUERY, description="Date in YYYY-MM-DD format", type=openapi.TYPE_STRING, required=True),
#         ],
#         responses={
#             200: openapi.Schema(
#                 type=openapi.TYPE_ARRAY,
#                 items=openapi.Items(
#                     type=openapi.TYPE_OBJECT,
#                     properties={
#                         "member_id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Member ID"),
#                         "member_name": openapi.Schema(type=openapi.TYPE_STRING, description="Member Name"),
#                         "available_times": openapi.Schema(
#                             type=openapi.TYPE_ARRAY,
#                             items=openapi.Items(type=openapi.TYPE_STRING),
#                             description="List of available times"
#                         ),
#                     }
#                 )
#             ),
#             404: openapi.Schema(
#                 type=openapi.TYPE_OBJECT,
#                 properties={
#                     "error": openapi.Schema(type=openapi.TYPE_STRING, description="Member not found")
#                 }
#             ),
#             400: openapi.Schema(
#                 type=openapi.TYPE_OBJECT,
#                 properties={
#                     "error": openapi.Schema(type=openapi.TYPE_STRING, description="Invalid input")
#                 }
#             )
#         },
#         operation_summary="Get All Members' Availability",
#         operation_description="Retrieves the availability of all members for a specific event and date, with the requesting user's data at the top."
#     )
#     def get(self, request):
#         user = request.user
#         try:
#             request_member = Member.objects.get(user=user)
#         except Member.DoesNotExist:
#             return Response(
#                 {"error": "Member not found for the current user."},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         event_id = request.query_params.get("event")
#         date_to_search = request.query_params.get("date")

#         if not event_id or not date_to_search:
#             return Response({"error": "Missing 'event' or 'date' parameter."}, status=400)

#         records = EventDateSelection.objects.filter(
#             event=event_id,
#             selected_dates__has_key=date_to_search
#         )

#         request_member_info = None
#         members = []

#         for record in records:
#             member = record.member
#             selected_dates = record.selected_dates
#             available_times = selected_dates.get(date_to_search, [])

#             member_info = {
#                 "member_id": member.id,
#                 "member_name": member.name,
#                 "available_times": available_times
#             }

#             if member == request_member:
#                 request_member_info = member_info
#             else:
#                 members.append(member_info)

#         if request_member_info:
#             result = [request_member_info] + members
#         else:
#             result = members

#         return Response(result, status=200)





class EventDateSelectionSearchView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'member', openapi.IN_QUERY,
                description="Member ID",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'event', openapi.IN_QUERY,
                description="Event ID",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'year', openapi.IN_QUERY,
                description="Year (YYYY format)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'month', openapi.IN_QUERY,
                description="Month (MM format)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'day', openapi.IN_QUERY,
                description="Day (DD format)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'hour', openapi.IN_QUERY,
                description="Hour (HH format)",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Items(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER, description="Record ID"),
                        "member": openapi.Schema(type=openapi.TYPE_INTEGER, description="Member ID"),
                        "event": openapi.Schema(type=openapi.TYPE_INTEGER, description="Event ID"),
                        "selected_dates": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            additional_properties=openapi.Schema(
                                type=openapi.TYPE_ARRAY,
                                items=openapi.Items(type=openapi.TYPE_STRING)
                            )
                        )
                    }
                )
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(type=openapi.TYPE_STRING, description="Error message")
                }
            ),
        },
        operation_summary="Filter Event Date Selections by Multiple Criteria",
        operation_description=(
            "Filters EventDateSelection records based on query parameters like member, event, year, month, day, or hour. "
            "If no parameters are provided, it returns all records."
        )
    )
    
    def get(self, request): 
        member_id = request.query_params.get("member")
        event_id = request.query_params.get("event")
        year = request.query_params.get("year")
        month = request.query_params.get("month")
        day = request.query_params.get("day")
        hour = request.query_params.get("hour")
        records = EventDateSelection.objects.all()
        if member_id:
            records = records.filter(member__id=member_id)
        if event_id:
            records = records.filter(event__id=event_id)
        if year or month or day or hour:
            filtered_records = []
            for record in records:
                for date, times in record.selected_dates.items():
                    parsed_date = datetime.strptime(date, "%Y-%m-%d")
                    
                    # 조건 확인
                    if year and parsed_date.year != int(year):
                        continue
                    if month and parsed_date.month != int(month):
                        continue
                    if day and parsed_date.day != int(day):
                        continue
                    if hour:
                        # 시간 조건 확인
                        hour_matches = any(time.startswith(f"{int(hour):02d}") for time in times)
                        if not hour_matches:
                            continue
                    
                    # 조건을 만족하면 추가
                    filtered_records.append(record)
                    break

            records = filtered_records

        
        serializer = EventDateSelectionSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EventDateSelectionAvailableUsersCountView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'event', openapi.IN_QUERY,
                description="Event ID to filter the results by event.",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'member', openapi.IN_QUERY,
                description="Filter results by the member ID.",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'year', openapi.IN_QUERY,
                description="Year (YYYY format), filters the results by year.",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'month', openapi.IN_QUERY,
                description="Month (MM format), filters the results by month.",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
            openapi.Parameter(
                'day', openapi.IN_QUERY,
                description="Day (DD format), filters the results by day.",
                type=openapi.TYPE_INTEGER,
                required=False
            ),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                additional_properties=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "2024-11-01": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "09:00": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "14:00": openapi.Schema(type=openapi.TYPE_INTEGER),
                            },
                        ),
                        "2024-11-02": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "10:00": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "15:00": openapi.Schema(type=openapi.TYPE_INTEGER),
                            },
                        ),
                    }
                )
            ),
            400: openapi.Response(
                description="Bad request, missing or invalid input parameters."
            ),
            404: openapi.Response(
                description="Event not found for the provided ID."
            ),
        },
        operation_summary="Get available users count by date and time",
        operation_description="Filters available user counts by year, month, or day, and returns the available users for each time slot per date. The 'event' parameter is required."
    )
    def get(self, request):
        event_id = request.query_params.get("event")
        member_id = request.query_params.get("member")
        year = request.query_params.get("year")
        month = request.query_params.get("month")
        day = request.query_params.get("day")

        # 기본적으로 모든 데이터 조회
        records = EventDateSelection.objects.all()
        if member_id:
            records = records.filter(member__id=member_id)
        if event_id:
            records = records.filter(event__id=event_id)

        # 결과를 저장할 딕셔너리
        available_users_count = {}

        # 각 레코드를 순회하며 날짜, 시간대 별 가능한 인원 수를 계산
        for record in records:
            for date, times in record.selected_dates.items():
                parsed_date = datetime.strptime(date, "%Y-%m-%d")
                
                # 날짜 필터링
                if year and parsed_date.year != int(year):
                    continue
                if month and parsed_date.month != int(month):
                    continue
                if day and parsed_date.day != int(day):
                    continue
                
                # 날짜 키가 없다면 생성
                if date not in available_users_count:
                    available_users_count[date] = {}

                # 시간대 필터링 및 카운팅
                for time in times:
                    if time not in available_users_count[date]:
                        available_users_count[date][time] = 0  # 시간대가 없으면 0으로 초기화

                    available_users_count[date][time] += 1

        # 결과 직렬화
        response_data = {}
        for date, time_counts in available_users_count.items():
            time_data = {time: count for time, count in time_counts.items() if count > 0}
            if time_data:
                response_data[date] = time_data

        return Response(response_data, status=status.HTTP_200_OK)