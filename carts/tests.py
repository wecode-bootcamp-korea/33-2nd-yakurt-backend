import json
import bcrypt
import jwt

from django.http import JsonResponse
from django.test import TestCase, Client
from django.conf import settings


from .models import Cart
from users.models import User
from products.models import Product

class CartTest(TestCase):
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
            information="필리 오메가3는 작은 어류를 원료로 사용하는 노르웨이산 프리미엄 rTG오메가3를 사용하고 우수한 품질관리를 통해 만들었습니다",
            name="오메가3",description="오메가입니당",
            image_url="https://img.pilly.kr/product/v20200519/omega3/tablet.png?v=v202111121657",
            price=13500,
            time="30일분",
            is_subscription=True
        )
        
    def tearDown(self):
        Cart.objects.all().delete()

    def test_cart_post_success(self):
        client = Client()
        header = {"HTTP_Authorization" :  'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.Ro8z9wYC94RH5eaNt0QxcUYZKd_wxQGzXRDVpYTw0do'}
        
        cart = {
            'id'        : 1,
            'product_id': 1,
            'quantity'  : 3,
            'is_user_survey' : True
        }

        response = client.post('/carts', json.dumps(cart), **header, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message' : "SUCCESS"})

class CartDeleteTest(TestCase):
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
    def tearDown(self):
        User.objects.all().delete()
        Product.objects.all().delete()
        Cart.objects.all().delete()
        
    def test_cart_delete_success(self):
        client = Client()
        header = {"HTTP_Authorization" : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.Ro8z9wYC94RH5eaNt0QxcUYZKd_wxQGzXRDVpYTw0do'}

        response = client.delete('/carts', **header)
        self.assertEqual(response.status_code, 204)

class CartShowTest(TestCase):
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
    def tearDown(self):
        User.objects.all().delete()
        Product.objects.all().delete()
        Cart.objects.all().delete()
        
    def test_cart_show_success(self):
        client = Client()
        header = {"HTTP_Authorization" : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MX0.Ro8z9wYC94RH5eaNt0QxcUYZKd_wxQGzXRDVpYTw0do'}

        results = [{
                "id"             : 1,
                "img"            : "test_url",
                "title"          : "오메가3",
                "quantity"       : 2,
                "price"          : 13500,
                "is_subscription": True,
                "is_user_survey" : False
            },
            {
                "id"             : 2,
                "img"            : "test_url",
                "title"          : "오메가3",
                "quantity"       : 1,
                "price"          : 13500,
                "is_subscription": True,
                "is_user_survey" : True
            }
            ]

        response = client.get('/carts', **header)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"carts": results})