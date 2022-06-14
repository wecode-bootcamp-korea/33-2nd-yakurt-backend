from django.urls import path

from subscriptions.views import Reviewdetailview

urlpatterns = [
    path('/<int:subscription_id>/review',Reviewdetailview.as_view()),
]