from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Marker, Member, Event
from core.serializers.marker import MarkerSerializer


class MarkerSaveView(APIView):
    def post(self, request):
        # 마커 데이터를 저장
        data = request.data.get("markers", [])
        for marker in data:
            Marker.objects.create(
                event_id=marker.get("event_id"),
                member_id=marker.get("member_id"),
                latitude=marker.get("latitude"),
                longitude=marker.get("longitude"),
                place_name=marker.get("place_name"),
            )
        return Response(
            {"message": "Markers saved successfully."}, status=status.HTTP_201_CREATED
        )


class MarkerListView(APIView):
    def get(self, request, event_id):
        # 특정 그룹의 모든 마커 반환
        markers = Marker.objects.filter(event_id=event_id)
        serializer = MarkerSerializer(markers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MarkerDeleteView(APIView):
    def delete(self, request, marker_id):
        marker = Marker.objects.filter(id=marker_id).first()
        if marker:
            marker.delete()
            return Response(
                {"message": "Marker deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )
        return Response(
            {"message": "Marker not found."}, status=status.HTTP_404_NOT_FOUND
        )
