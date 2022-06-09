import json, requests, jwt

from django.shortcuts import redirect
from django.http  import JsonResponse
from django.views import View
from django.conf  import settings

from users.models import User

class KakaoSignInView(View):
    def get(self, request):
        kakao_api = 'https://kauth.kakao.com/oauth/authorize?response_type=code'
        redirect_uri = settings.KAKAO_REDIRECT_URI
        client_id = settings.KAKAO_CLIENT_ID
        
        return redirect(f'{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}')

class kakaoCallBackView(View):
    def get(self,request):
        data = {
            'grant_type'     : 'authorization_code',
            'redirection_uri': settings.KAKAO_REDIRECT_URI,
            'client_id'      : settings.KAKAO_CLIENT_ID,
            'code'           : request.GET['code']
        }
        
        kakao_token_api = 'https://kauth.kakao.com/oauth/token'
        access_token = requests.post(kakao_token_api, data=data).json()['access_token']
                
        kakao_user_info_api = 'https://kapi.kakao.com/v2/user/me'
        user_info_response  = requests.get(kakao_user_info_api, headers={'Authorization' : f'Bearer {access_token}'}).json()
        kakao_id  = user_info_response['id']
        nick_name = user_info_response['properties']['nickname']
        email     = user_info_response['kakao_account']['email']
        
        user, is_created = User.objects.get_or_create(
                kakao_id = kakao_id,
                defaults = {
                    'nick_name': nick_name,
                    'email'    : email
                }
        )
        
        data = {
            'access_token': jwt.encode({'id' : user.id}, settings.SECRET_KEY, settings.ALGORITHM),
            'nick_name'   : nick_name,
            'email'       : email
        }
        
        return JsonResponse({'Message' : 'SUCCESS', 'data' : data}, status = 200)

        