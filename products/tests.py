import json

from django.http import response
from django.test import TestCase, Client

from products.models      import Product, ProductEffect, Effect
from subscriptions.models import SubscriptionItem, Subscription, Review
from orders.models        import PaymentMethod
from users.models         import User

TestCase.maxDiff = None
class ProductDetailTest(TestCase):
    def setUp(self):
        Product.objects.create(
            id              = 1,
            title           = '상품 1 제목',
            information     = '상품 1 설명',
            name            = '상품 1 이름',
            description     = '상품 1 정보',
            image_url       = 'image_url',
            price           = '11111',
            time            = '30일분',
            is_subscription = 1,
        )
        
        Effect.objects.create(
            id   = 1,
            name = '이펙트 1'
        )
        
        Effect.objects.create(
            id   = 2,
            name = '이펙트 2'
        )

        ProductEffect.objects.create(
            id         = 1,
            product_id = 1,
            effect_id  = 1
        )
        
        ProductEffect.objects.create(
            id         = 2,
            product_id = 1,
            effect_id  = 2
        )
        
        PaymentMethod.objects.create(
            id      = 1,
            payment = 'CARD'
        )
        
        User.objects.create(
            id        = 1,
            kakao_id  = 123456790,
            email     = 'test1234@kakao.com',
            nick_name = 'test'
        )
        
        Subscription.objects.create(
            id                = 1,
            is_subscribing    = 1,
            delivery_message  = 1,
            payment_method_id = 1,
            user_id           = 1
        )
        
        SubscriptionItem.objects.create(
            id              = 1,
            quantity        = 1,
            product_id      = 1,
            subscription_id = 1
        )

        Review.objects.create(
            id              = 1,
            content         = '리뷰테스트',
            subscription_id = 1,
            user_id         = 1
        )

    def tearDown(self):
        Product.objects.all().delete()

    def test_success_productdetailview_get(self):
        client = Client()

        response = client.get('/products/1')
        print(response)
        self.assertEqual(response.json(),
            {
                'results' : [{
                            'id'             : 1,
                            'title'          : '상품 1 제목',
                            'information'    : '상품 1 설명',
                            'name'           : '상품 1 이름',
                            'description'    : '상품 1 정보',
                            'image_url'      : 'image_url',
                            'price'          : '11111.00',
                            'time'           : '30일분',
                            'is_subscription': True,
                            'review_count'   : 1,
                            'product_effect' : ['이펙트 1','이펙트 2']
                    }]
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_fail_productdetailview_get_product_id_not_exist(self):
        client = Client()

        response = client.get('/products/99')

        self.assertEqual(response.json(),
            {'Message': 'PRODUCT_DOES_NOT_EXIST'}
        )
        self.assertEqual(response.status_code, 404)