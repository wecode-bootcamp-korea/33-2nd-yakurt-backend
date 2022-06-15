from django.urls import path

from .views import OrderView,OrderDetailView

urlpatterns = [
    path('', OrderView.as_view()),
    path('/<str:order_number>', OrderDetailView.as_view())
]