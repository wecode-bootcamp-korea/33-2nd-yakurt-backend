from django.db import models

from core.models import TimeStampedModel

class User(TimeStampedModel):
    kakao_id        = models.BigIntegerField()
    email           = models.CharField(max_length=100, unique=True)
    nick_name       = models.CharField(max_length=30, null=True)
    phone_number    = models.CharField(max_length=30, null=True)
    address         = models.CharField(max_length=200, null=True)
    phone_subscribe = models.BooleanField(default=False)
    email_subscribe = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'users'
