from django.urls import path

from users.views import kakaoCallBackView

urlpatterns = [
    path('/kakao/callback',kakaoCallBackView.as_view()),
]