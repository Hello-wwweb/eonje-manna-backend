from django.db import models

from common.models.timestamped_model import TimeStampedModel


class Member(TimeStampedModel):
    user = models.ForeignKey('core.CustomUser', on_delete=models.PROTECT)

    class Meta:
        db_table = 'member'
        verbose_name = "멤버"
