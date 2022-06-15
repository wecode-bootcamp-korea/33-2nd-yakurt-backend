import json
import uuid

from django.views         import View
from django.http          import JsonResponse
from django.db            import transaction
from django.db.models     import F, Sum, DecimalField

from core.utils           import login_decorator
from carts.models         import Cart
from subscriptions.models import Subscription
from users.models         import User
from orders.models        import Order,OrderItem,PaymentMethod
from subscriptions.models import Subscription,SubscriptionItem
from products.models      import Product

class OrderView(View):
    @login_decorator
    def post(self, request):
        try: 
            data              = json.loads(request.body)
            user              = request.user
            delivery_message  = data['delivery_message']
            payment_method_id = data['payment_method_id']
            select_cart       = data['select_cart']
            carts             = Cart.objects.filter(user=user, id__in=select_cart)

            if not carts:
                return JsonResponse({'message': 'EMPTY_CART'}, status=400)
           
            with transaction.atomic():
                order = Order.objects.create(
                    order_number     = uuid.uuid4(),
                    user_id          = user.id,
                    delivery_message = delivery_message,
                    payment_method_id= payment_method_id
                )

                for cart in carts:
                    OrderItem.objects.create(
                        order    = order,
                        product  = cart.product,
                        quantity = cart.quantity
                )

                for item in order.orderitem_set.all():
                    if item.product.is_subscription:
                        subscription = Subscription.objects.create(
                            user_id           = user.id,
                            delivery_message  = delivery_message,
                            payment_method_id = payment_method_id
                        )
                
                        SubscriptionItem.objects.create(
                            subscription = subscription,
                            product      = item.product,
                            quantity     = item.quantity
                        )
           
                carts.delete()

                response = {
                    "message" : "created",
                    "data"    : {
                        "order_id"     : order.id,
                        "order_number" : order.order_number
                    }
                }
                return JsonResponse(response, status=201)
                
        except transaction.TransactionManagementError:
            return JsonResponse({'message':'TransactionManagementError'}, status=400)  
        except KeyError:
            return JsonResponse({"message" : "KEYERROR"}, status=400)

class OrderDetailView(View):
    @login_decorator
    def get(self, request, order_number):

        orders = Order.objects.filter(user=request.user, order_number=order_number)

        results = [{
            'order_number': order.order_number,
            'order_date'  : order.created_at,
            'product'     : [{
            'order_item': orderitem.product.name,
            'quantity'  : orderitem.quantity,
            'price'     : orderitem.product.price,
            } for orderitem in order.orderitem_set.all()],
            'total_bill'      : order.orderitem_set.aggregate(item_price=Sum(F('product__price') * F('quantity') * 0.09 + 2500, output_field = DecimalField()))['item_price'],
            'user_name'       : order.user.nick_name,
            'user_address'    : order.user.address,
            'user_phonenumber': order.user.phone_number,
            'payment_method'  : order.payment_method.payment
        } for order in orders]

        return JsonResponse({'results': results}, status=200)