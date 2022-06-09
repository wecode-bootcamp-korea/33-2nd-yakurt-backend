import json, jwt

from unittest.mock import patch, MagicMock

from django.conf   import settings
from django.test   import TestCase, Client

from .models  import *

class KakaoSignInTest(TestCase):
    def setUp(self):
        User.objects.create(
            kakao_id  = "123123",
            nick_name = "test",
            email     = "test@gmail.com",
        )

    def tearDown(self):
        User.objects.all().delete()
    
class SignInTest(TestCase):
    @patch('users.views.requests')
    def test_kakao_signin_view_get_success(self, mocked_requests):
            client = Client()

            class MockedResponse:
                status_code = 200
                
                def json(self):
                    return {
                        "id": 2145645622,
                        "connected_at": "2022-06-09T20:48:20Z",
                        "properties": {"nickname": "test"},
                        "email": "test@gmail.com",
                    }

            mocked_requests.get = MagicMock(return_value = MockedResponse())
            headers = {"HTTP_Authorization" : "123123"}
            response = client.get("/users/kakao", **headers)

            self.assertEqual(response.status_code, 201 | 200) 
            
    @patch('users.views.requests')
    def test_kakao_signin_fail_key_error(self, mocked_requests):
        client = Client()
        
        class MockedResponse:
            status_code = 400

            def json(self):
                return {
                    'id' : 123456789,
                    'kakao_account' : {
                        'profile' : {
                            'nickname' : 'test'
                        }
                    }
                }
        
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'Authorization' : '123456789'}
        response            = client.get('/users/kakao', **headers)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'message' : 'Key error'})


    @patch('users.views.requests')
    def test_kakao_signin_invaild_token_error(self, mocked_requests):
        client = Client()

        class MockedResponse:
            status_code = 401
            def json(self):
                return {'msg': 'no authentication key!', 'code': -401}
        
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers  = {'Authorizaton' : "123456789"} 
        response = client.get("/users/kakao", **headers)
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {'message' : 'Invalid token'})