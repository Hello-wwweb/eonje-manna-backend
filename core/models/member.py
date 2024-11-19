from django.db import models

from common.models.timestamped_model import TimeStampedModel


class Member(TimeStampedModel):
    user = models.OneToOneField("core.User", on_delete=models.PROTECT)
    name = models.CharField(max_length=120)
    email = models.CharField(max_length=120, unique=True)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "member"
        verbose_name = "멤버"
