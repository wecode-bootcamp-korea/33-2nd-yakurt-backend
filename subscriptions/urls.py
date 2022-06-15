from django.urls import path

from subscriptions.views import Reviewlistview, SubscriptionListview, Reviewdetailview

urlpatterns = [
    path('/<int:subscription_id>/review',Reviewdetailview.as_view()),
    path('',SubscriptionListview.as_view()),
    path('/reviews',Reviewlistview.as_view()),
]