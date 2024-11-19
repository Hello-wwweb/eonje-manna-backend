from django.db import models

from common.models.timestamped_model import TimeStampedModel


class EventLocationSelection(TimeStampedModel):
    member = models.ForeignKey("core.Member", on_delete=models.PROTECT)
    event = models.ForeignKey("core.Event", on_delete=models.PROTECT)
    selected_places = models.JSONField()

    class Meta:
        db_table = "event_location_selection"
        verbose_name = "이벤트 장소 선택"
