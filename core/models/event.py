from django.db import models

from common.models.timestamped_model import TimeStampedModel


class Event(TimeStampedModel):
    group = models.ForeignKey("core.MeetingGroup", on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    event_date = models.DateTimeField(null=True)
    event_location = models.CharField(max_length=255, null=True)
    created_by = models.ForeignKey("core.User", on_delete=models.PROTECT)

    class Meta:
        db_table = "event"
        verbose_name = "이벤트"
