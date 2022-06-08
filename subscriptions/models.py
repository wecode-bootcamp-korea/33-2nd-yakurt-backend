from django.db import models

from core.models import TimeStampedModel

class Subscription(TimeStampedModel):
    user             = models.ForeignKey('users.User', on_delete=models.CASCADE)
    is_subscribing   = models.BooleanField(default=True)
    delivery_message = models.CharField(max_length=100)
    payment_method    = models.ForeignKey('orders.Paymentmethod', on_delete=models.CASCADE)

    class Meta:
        db_table = 'subscriptions'

class SubscriptionItem(TimeStampedModel):
    quantity     = models.IntegerField()
    product      = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    subscription = models.ForeignKey('Subscription', on_delete=models.CASCADE)

    class Meta:
        db_table = 'subscription_items'

class Review(TimeStampedModel):
    user         = models.ForeignKey('users.User', on_delete=models.CASCADE)
    content      = models.CharField(max_length=100)
    image_url    = models.CharField(max_length=1000)
    subscription = models.ForeignKey('subscriptions.Subscription', on_delete=models.CASCADE)

    class Meta:
        db_table = 'reviews'