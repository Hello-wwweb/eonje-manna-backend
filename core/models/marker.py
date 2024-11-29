from django.db import models


class Marker(models.Model):
    event_id = models.CharField(max_length=50)  # 그룹 ID
    member_id = models.CharField(max_length=50)
    latitude = models.FloatField()  # 위도
    longitude = models.FloatField()  # 경도
    place_name = models.CharField(max_length=255)  # 장소 이름
    created_at = models.DateTimeField(auto_now_add=True)  # 생성 시간

    def __str__(self):
        return f"Marker by {self.member_id} in Group {self.group_id}: ({self.latitude}, {self.longitude})"
