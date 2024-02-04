# api/views.py
from rest_framework import status
from data_engine_api.models import CustomerRevenue
from data_engine_api.serializers import CustomerRevenueSerializer
from rest_framework import mixins
from rest_framework import generics
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

class CustomerRevenueList(generics.ListAPIView):
    serializer_class = CustomerRevenueSerializer
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        user = self.request.user
        customer_id = False
        if user.is_superuser:
            customer_id = self.request.GET.get("customer_id")
        elif not user.is_anonymous and hasattr(user, 'customer'):
            customer_id = user.customer.id
        if customer_id:
            return CustomerRevenue.objects.filter(customer_id=customer_id)
        return CustomerRevenue.objects.none()


    
