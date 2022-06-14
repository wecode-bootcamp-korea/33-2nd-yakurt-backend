from django.http  import JsonResponse
from django.views import View

from products.models import Product

class ProductDetailView(View):
    def get(self, request, product_id):
        if not Product.objects.filter(id=product_id).exists():
            return JsonResponse({'Message': 'PRODUCT_DOES_NOT_EXIST'}, status=404)
        
        product = Product.objects.filter(id=product_id)

        results = [{
            'id'             : product.id,
            'title'          : product.title,
            'information'    : product.information,
            'name'           : product.name,
            'description'    : product.description,
            'image_url'      : product.image_url,
            'price'          : product.price,
            'time'           : product.time,
            'is_subscription': product.is_subscription,
            'review_count'   : product.subscriptionitem_set.all().first().subscription.review_set.count(),
            'product_effect' : [effect.name for effect in product.effect_set.all()]
        } for product in product]

        return JsonResponse({'results': results}, status=200)

class ProductListView(View):
    def get(self, request):
        offset   = int(request.GET.get('offset', 0))
        limit    = int(request.GET.get('limit', 15))
        products = Product.objects.all()[offset:offset+limit]
        
        results = [{
            'id'             : product.id,
            'title'          : product.title,
            'information'    : product.information,
            'name'           : product.name,
            'description'    : product.description,
            'image_url'      : product.image_url,
            'price'          : product.price,
            'time'           : product.time,
            'is_subscription': product.is_subscription,
            'product_effect' : [effect.name for effect in product.effect_set.all()]
        }for product in products]

        return JsonResponse({'results': results}, status=200)