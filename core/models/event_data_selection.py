from django.db import models

from common.models.timestamped_model import TimeStampedModel


class EventDateSelection(TimeStampedModel):
    member = models.ForeignKey("core.Member", on_delete=models.PROTECT)
    event = models.ForeignKey("core.Event", on_delete=models.PROTECT)
    selected_dates = models.JSONField()

    class Meta:
        db_table = "event_data_selection"
        verbose_name = "이벤트 날짜 선택"
