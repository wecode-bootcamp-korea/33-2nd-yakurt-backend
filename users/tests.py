from unittest.mock import patch, MagicMock

from django.test   import TestCase, Client

from users.models  import User

class KakaoSignInTest(TestCase):
    def setUp(self):
        user = User.objects.create(
            kakao_id  = '1234567890',
            nick_name = 'test',
            email     = 'test@gmail.com'
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
                    'id': '987654321',
                    'properties': {
                        'nickname': 'test'
                    },
                    'profile': {
                        'email': 'test@gmail.com',
                    }
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
                    'id' : 2145645622,
                    'kakao_account' : {
                        'profile' : {
                            'nickname' : 'test'
                        }
                    }
                }
        
        mocked_requests.get = MagicMock(return_value = MockedResponse())
        headers             = {'Authorization' : '123123'}
        response            = client.get('/users/kakao', **headers)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'Message' : 'Key error'})