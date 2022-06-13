from django.urls import path

from users.views import kakaoCallBackView, UserView

urlpatterns = [
    path('/kakao/callback',kakaoCallBackView.as_view()),
    path('',UserView.as_view()),
]