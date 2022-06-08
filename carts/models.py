from django.db import models

from core.models import TimeStampedModel

class Cart(TimeStampedModel):
    user           = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product        = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity       = models.IntegerField()
    is_user_survey = models.BooleanField()

    class Meta:
        db_table = 'carts'