# api/serializers.py
from rest_framework import serializers
from data_engine_api.models import CustomerRevenue

class CustomerRevenueSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerRevenue
        fields = '__all__'