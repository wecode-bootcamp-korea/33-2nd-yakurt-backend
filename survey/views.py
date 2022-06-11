import json

from django.http  import JsonResponse
from django.views import View

from survey.models import UserSurvey, SurveyProduct
from core.utils    import login_decorator

class UserSurveyView(View):
    @login_decorator
    def post(self, request):
        try:
            data       = json.loads(request.body)
            user       = request.user
            gender     = data['gender']
            age        = data['age']
            weight     = data['weight']
            height     = data['height']
            product_id = data['product_id']

            user_survey = UserSurvey.objects.create(
                user   = user,
                gender = gender,
                age    = age,
                weight = weight,
                height = height,
            )
            
            survey_products = [
                SurveyProduct(
                    user_survey_id = user_survey.id,
                    product_id     = product_id[i],
                ) for i in product_id 
            ]
            SurveyProduct.objects.bulk_create(survey_products)

            return JsonResponse({'Message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'Message': 'KEY_ERROR'}, status=400)