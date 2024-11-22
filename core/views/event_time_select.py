# 사용자가 event를 고르고 시간을 정한 뒤 요청을 보내면 -> 그 사람이 만든 요청을 서버에 저장해야함  
# 저장된 정보를 요청하면 보내주기(사용자 별로 다르게 보내줘야함) + 교집합으로 가능한 날짜 및 시간을 가공해서 보내주기 
from core.models.member import Member
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.models import EventDateSelection
from core.serializers.event_time_selection import EventDateSelectionRequestSerializer,EventDateSelectionSerializer

class EventDateSelectionView(APIView):
    @swagger_auto_schema(
        request_body=EventDateSelectionSerializer,  # 요청 본문을 설명
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
            # 유효한 데이터를 저장하기 위해 EventDateSelection 객체 생성
            validated_data = serializer.validated_data
            event_id = validated_data['event']
            selected_dates = validated_data['selected_dates']
            
            # EventDateSelection 저장
            event_date_selection = EventDateSelection.objects.create(
                member=member,
                event_id=event_id,  # event_id로 저장
                selected_dates=selected_dates
            )

            # 직렬화하여 응답 데이터 생성
            response_serializer = EventDateSelectionSerializer(event_date_selection)
            response_data = response_serializer.data

            return Response(response_data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class EventDateSelectionDetailView(APIView): 
    def get_object(self, pk):
        try:
            obj = EventDateSelection.objects.get(pk=pk)
            return obj
        except EventDateSelection.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self,request,pk):
        obj = self.get_object(pk)
        serializer = EventDateSelectionSerializer(obj)
        return Response(serializer.data) 
    
