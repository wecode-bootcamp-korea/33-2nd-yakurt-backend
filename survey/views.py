import json

from django.http  import JsonResponse
from django.views import View

from survey.models import UserSurvey, SurveyProduct
from core.utils    import login_decorator

class UserSurveyView(View):
    @login_decorator
    def post(self, request):
        try:
            data        = json.loads(request.body)
            user        = request.user
            gender      = data['gender']
            age         = data['age']
            weight      = data['weight']
            height      = data['height']
            product_ids = data['product_id']

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
                    product_id     = product_id,
                ) for product_id in product_ids 
            ]
            SurveyProduct.objects.bulk_create(survey_products)

            return JsonResponse({'Message': 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'Message': 'KEY_ERROR'}, status=400)

    @login_decorator
    def get(self, request):
        offset = int(request.GET.get('offset', 0))
        limit  = int(request.GET.get('limit', 15))
        user   = request.user
        
        user_survey = UserSurvey.objects.filter(user_id = user.id)[offset:offset+limit]
        
        results = [{
            'user_survey_id' : user_survey.id,
            'user_survey_created_at' : user_survey.created_at,
            'survey_product': [surveyproduct.product.name for surveyproduct in user_survey.surveyproduct_set.all()]
        }for user_survey in user_survey]
        
        return JsonResponse({'results': results}, status=200)