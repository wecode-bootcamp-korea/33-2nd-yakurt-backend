from django.urls import path

from survey.views import UserSurveyView, UserSurveyDetailView, UserSurveyListDetailView

urlpatterns = [
    path('',UserSurveyView.as_view()),
    path('/<int:user_survey_id>',UserSurveyListDetailView.as_view()),
    path('/last',UserSurveyDetailView.as_view()),
]