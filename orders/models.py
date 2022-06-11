from django.db import models

from core.models import TimeStampedModel

class Order(TimeStampedModel):
    order_number     = models.CharField(max_length=100)
    user             = models.ForeignKey('users.User', on_delete=models.CASCADE)
    delivery_message = models.CharField(max_length=100)
    payment_method    = models.ForeignKey('Paymentmethod', on_delete=models.CASCADE)

    class Meta:
        db_table = 'orders'

class OrderItem(TimeStampedModel):
    quantity     = models.IntegerField()
    product      = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    order        = models.ForeignKey('Order', on_delete=models.CASCADE)

    class Meta:
        db_table = 'order_items'

class PaymentMethod(TimeStampedModel):
    payment = models.CharField(max_length=10)

    class Meta:
        db_table = 'paymentmethod'