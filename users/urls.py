from django.urls import path

from users.views import KakaoSignInView, kakaoCallBackView

urlpatterns = [
    path('/kakao',KakaoSignInView.as_view()),
    path('/kakao/callback',kakaoCallBackView.as_view()),

]