
import json

from django.views import View
from django.http import JsonResponse

from core.utils import login_decorator
from carts.models import Cart
from products.models import Product
from survey.models import SurveyProduct


class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            data           = json.loads(request.body)
            user           = request.user
            product_id     = data['product_id']
            quantity       = data['quantity']
           
            if not Product.objects.get(id=product_id):
                return JsonResponse({'message': 'PRODUCT_NOT_EXIST'}, status=400)
        
            if quantity <= 0:
                return JsonResponse({'message':'QUANTITY_ERROR'}, status=400)


            cart, created = Cart.objects.get_or_create(
                user_id    = user.id,
                product_id = product_id,
                defaults    = {
                    'quantity'      : quantity,
                    'is_user_survey': True if SurveyProduct.objects.filter(product_id=product_id).exists() else False
                }
            )

            if not created:
                cart.quantity += 1
                cart.save()

            return JsonResponse({'message' : "SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

