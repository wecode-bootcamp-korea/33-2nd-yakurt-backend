from django.urls import path

from survey.views import UserSurveyView

urlpatterns = [
    path('/user',UserSurveyView.as_view()),
]