from django.urls import path
from .views import CustomerRevenueList

urlpatterns = [
    path('revenue_list/', CustomerRevenueList.as_view(), name='customer_revenew'),
]