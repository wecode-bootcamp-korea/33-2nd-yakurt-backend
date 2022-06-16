import json
import bcrypt
import jwt

from django.http import JsonResponse
from django.test import TestCase, Client
from django.conf import settings
from freezegun import freeze_time

from carts.models    import Cart
from .models         import Order, OrderItem, PaymentMethod
from users.models    import User
from products.models import Product

class OrderPostTest(TestCase):
    def setUp(self):
        User.objects.create(
            id = 1,
            kakao_id ='128738174',
            email = 'test@mail.com',
            nick_name = 'test'
        )
        Product.objects.create(
            id = 1,
            title="혈행개선/눈 건강을 위한 필리 오메가3",
            information="필리 오메가3는",
            name="오메가3",
            description="오메가입니당",
            image_url="test_url",
            price=13500,
            time="30일분",
            is_subscription=True
        )
        Product.objects.create(
            id = 2,
            title="혈행개선/눈 건강을 위한 필리 오메가3",
            information="필리 오메가3는",
            name="오메가3",
            description="오메가입니당",
            image_url="test_url",
            price=13500,
            time="30일분",
            is_subscription=True
        )
        Cart.objects.create(
            id = 1,
            user_id = 1,
            product_id = 1,
            quantity = 2,
            is_user_survey = 0
        )
        Cart.objects.create(
            id = 2,
            user_id = 1,
            product_id = 2,
            quantity = 1,
            is_user_survey = 1
        )
        PaymentMethod.objects.create(
            id      = 1,
            payment = 1
        )
    def tearDown(self):
        Cart.objects.all().delete()

    def test_order_post_success(self):
        client = Client()
        header = {"HTTP_Authorization" : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.Ro8z9wYC94RH5eaNt0QxcUYZKd_wxQGzXRDVpYTw0do'}
        
        order = {
            "select_cart"      : [1,2],
            "delivery_message" : "오늘은 목요일",
            "payment_method_id": 1
         }

        response = client.post('/orders', json.dumps(order), **header, content_type='application/json')
        self.assertEqual(response.status_code, 201)

@freeze_time("2021-01-01")
class OrdeGetTest(TestCase):

    maxDiff = None

    def setUp(self):
        User.objects.create(
            id = 1,
            kakao_id ='128738174',
            email = 'test@mail.com',
            nick_name = 'test',
            address = '선릉역',
            phone_number = '123456'
        )
        Product.objects.create(
            id = 1,
            title="혈행개선/눈 건강을 위한 필리 오메가3",
            information="필리 오메가3는",
            name="오메가3",
            description="오메가입니당",
            image_url="test_url",
            price=13500.00,
            time="30일분",
            is_subscription=True
        )
        PaymentMethod.objects.create(
            id      = 1,
            payment = "카카오페이"
        )
        Order.objects.create(
            order_number = '1243456',
            user_id = 1,
            delivery_message = "집에 가고 싶어라",
            payment_method_id = 1
        )
        OrderItem.objects.create(
            quantity = 1,
            product_id = 1,
            order_id = 1
        )
    def tearDown(self):
        User.objects.all().delete()
        Product.objects.all().delete()
        PaymentMethod.objects.all().delete()
        Order.objects.all().delete()
        OrderItem.objects.all().delete()

    def test_order_get_success(self):
        client = Client()
        header = {"HTTP_Authorization" : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.Ro8z9wYC94RH5eaNt0QxcUYZKd_wxQGzXRDVpYTw0do'}

        results = [{
            'order_number': '1243456',
            'order_date': '2021-01-01T00:00:00Z',
            'product'     : [{
                'order_item': '오메가3',
                'img'       : "test_url",
                'quantity'  : 1,
                'price'     : 13500.00}],
            'total_bill'      : 14650,
            'user_name'       : 'test',
            'user_address'    : '선릉역',
            'user_phonenumber': '123456',
            'delivery_message': '집에 가고 싶어라',
            'payment_method'  : '카카오페이'}]

        print(f"tests results :: ", results)

        response = client.get('/orders', **header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"results": results})