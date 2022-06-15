import json

from freezegun import freeze_time
from datetime import datetime

from django.http import response
from django.test import TestCase, Client

from products.models      import Product
from subscriptions.models import Subscription, Review, SubscriptionItem
from orders.models        import PaymentMethod
from users.models         import User

TestCase.maxDiff = None

@freeze_time("2021-01-01")
class ReviewListDetailTest(TestCase):
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

        User.objects.create(
            id        = 1,
            kakao_id  = 123456790,
            email     = 'test1234@kakao.com',
            nick_name = 'test'
        )
        
        PaymentMethod.objects.create(
            id      = 1,
            payment = 'CARD'
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
            image_url       = '리뷰 image_url',
            subscription_id = 1,
            user_id         = 1
        )

    def tearDown(self):
        Review.objects.all().delete()

    def test_success_reviewlistdetailview_get(self):
        client = Client()

        response = client.get('/subscriptions/review/1')

        self.assertEqual(response.json(),
            {
                'results' : {
                    "id": 1,
                    "nick_name": "test",
                    "content": "리뷰테스트",
                    "image_url": "리뷰 image_url",
                    "create_at": "2021-01-01T00:00:00Z",
                    "subscriptions_months": 0,
                    "products": [
                        {
                            "product_id": 1,
                            "product_title": "상품 1 제목",
                            "product_information": "상품 1 설명",
                            "product_image_url": "image_url"
                         }
                    ]
                }
            }
        )
        self.assertEqual(response.status_code, 200)

    def test_fail_review_list_detail_view_get_review_id_not_exist(self):
        client = Client()

        response = client.get('/subscriptions/review/99')

        self.assertEqual(response.json(),
            {'Message': 'REVIEW_DOES_NOT_EXIST'}
        )
        self.assertEqual(response.status_code, 404)