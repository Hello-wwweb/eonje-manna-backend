from django.db import models

from common.models.timestamped_model import TimeStampedModel


class Vote(TimeStampedModel):
    member = models.ForeignKey("core.Member", on_delete=models.PROTECT, null = True)
    event = models.ForeignKey("core.Event", on_delete=models.PROTECT)
    voted_places = models.CharField(max_length=500)

    class Meta:
        db_table = "vote"
        verbose_name = "투표"
