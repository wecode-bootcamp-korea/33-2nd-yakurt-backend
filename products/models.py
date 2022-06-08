from django.db import models

from core.models import TimeStampedModel

class Product(TimeStampedModel):
    title           = models.CharField(max_length=100)
    information     = models.CharField(max_length=500)
    name            = models.CharField(max_length=200)
    description     = models.CharField(max_length=2000)
    image_url       = models.CharField(max_length=1000)
    price           = models.DecimalField(max_digits=8,decimal_places=2)
    time            = models.CharField(max_length=100)
    is_subscription = models.BooleanField()

    class Meta:
        db_table = 'products'

class Effect(TimeStampedModel):
    name     = models.CharField(max_length=20)
    products = models.ManyToManyField('Product', through= 'ProductEffect')

    class Meta:
        db_table = 'effects'

class ProductEffect(TimeStampedModel):
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    effect  = models.ForeignKey('Effect', on_delete=models.CASCADE)

    class Meta:
        db_table = 'product_effects'