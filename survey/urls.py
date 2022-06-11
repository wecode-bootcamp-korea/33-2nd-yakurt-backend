from django.urls import path

from survey.views import UserSurveyListView

urlpatterns = [
    path('',UserSurveyListView.as_view()),
]