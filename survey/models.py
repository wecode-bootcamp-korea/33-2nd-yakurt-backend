from django.db import models

from core.models import TimeStampedModel

class UserSurvey(TimeStampedModel):
     user   = models.ForeignKey('users.User', on_delete=models.CASCADE)
     gender = models.CharField(max_length=10)
     age    = models.IntegerField()
     weight = models.DecimalField(max_digits=5,decimal_places=2)
     height = models.DecimalField(max_digits=5,decimal_places=1)

     class Meta:
         db_table = 'user_survey'

class SurveySymptom(TimeStampedModel):
    name     = models.CharField(max_length=200)
    products = models.ManyToManyField('products.Product', through= 'SymptomProduct')

    class Meta:
        db_table = 'survey_symptoms'

class SymptomProduct(TimeStampedModel):
    survey_symptom = models.ForeignKey('SurveySymptom', on_delete=models.CASCADE)
    product        = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    class Meta: 
        db_table = 'symptom_products'

class SurveyProduct(TimeStampedModel):
    user_survey = models.ForeignKey('UserSurvey', on_delete=models.CASCADE)
    product     = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    class Meta: 
        db_table = 'survey_products'
