from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import requests

from core.models import EventLocationSelection
from rest_framework.parsers import JSONParser
from core.serializers.event_location_selection import EventLocationSelectionSerializer


class EventLocationSelectionView(APIView):
    parser_classes = (JSONParser,)

    @swagger_auto_schema(
        operation_description="Post latitude, longitude, and optional address to get or validate address information.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "latitude": openapi.Schema(
                    type=openapi.TYPE_NUMBER, description="Latitude of the location"
                ),
                "longitude": openapi.Schema(
                    type=openapi.TYPE_NUMBER, description="Longitude of the location"
                ),
                "member_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="Member ID"
                ),
                "event_id": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="Event ID"
                ),
            },
            required=["latitude", "longitude", "member_id", "event_id"],
        ),
        responses={
            200: openapi.Response(
                "Successful response", EventLocationSelectionSerializer
            ),
            400: openapi.Response("Bad request, invalid input parameters"),
        },
    )
    def post(self, request):
        latitude = request.data.get("latitude")
        longitude = request.data.get("longitude")
        member_id = request.data.get("member_id")
        event_id = request.data.get("event_id")

        # 카카오 지도 API 호출
        try:
            headers = {"Authorization": "f406fe311a2173d0935a4362f3d563ab"}
            url = f"https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x={longitude}&y={latitude}"
            response = requests.get(url, headers=headers)
            reverse_geocode_result = response.json()

            if "error" in reverse_geocode_result:
                return Response(
                    {"error": reverse_geocode_result.get("error")},
                    status=reverse_geocode_result.get(
                        "status_code", status.HTTP_500_INTERNAL_SERVER_ERROR
                    ),
                )

            # 주소 정보 파싱
            address = reverse_geocode_result["documents"][0]["address"]["address_name"]
        except Exception as e:
            return Response(
                {"error": f"Failed to fetch address: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # 장소 데이터 생성
        place_data = {
            "member": member_id,
            "event": event_id,
            "latitude": latitude,
            "longitude": longitude,
            "address": address,
        }

        # 직렬화 및 저장
        serializer = EventLocationSelectionSerializer(data=place_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # 유효성 검사 실패 시 오류 반환
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        # 모든 위치 선택 데이터 조회
        selections = EventLocationSelection.objects.all()
        # 데이터를 직렬화
        serializer = EventLocationSelectionSerializer(selections, many=True)
        # 직렬화된 데이터를 클라이언트에 반환
        return Response(serializer.data, status=status.HTTP_200_OK)
