from django.db import models

from common.models.timestamped_model import TimeStampedModel


class MeetingGroup(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey('core.Member', on_delete=models.PROTECT)

    class Meta:
        db_table = 'meeting_group'
        verbose_name = '모임'
