from django.db import models

from common.models.timestamped_model import TimeStampedModel


class Membership(TimeStampedModel):
    member = models.ForeignKey("core.Member", on_delete=models.PROTECT)
    group = models.ForeignKey("core.MeetingGroup", on_delete=models.CASCADE)
    nickname = models.CharField(max_length=120)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "membership"
        verbose_name = "모임 멤버"
