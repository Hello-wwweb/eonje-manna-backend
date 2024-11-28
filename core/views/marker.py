from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models.marker import Marker
from core.serializers.marker import MarkerSerializer


class MarkerSaveView(APIView):
    def post(self, request):
        # 마커 데이터를 저장
        data = request.data.get("markers", [])
        for marker in data:
            Marker.objects.create(
                group_id=marker.get("group_id"),
                member_id=marker.get("member_id"),
                latitude=marker.get("latitude"),
                longitude=marker.get("longitude"),
                address=marker.get("address"),
            )
        return Response(
            {"message": "Markers saved successfully."}, status=status.HTTP_201_CREATED
        )


class MarkerListView(APIView):
    def get(self, request, group_id):
        # 특정 그룹의 모든 마커 반환
        markers = Marker.objects.filter(group_id=group_id)
        serializer = MarkerSerializer(markers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
