from django.test import TestCase
from decimal import Decimal
from datetime import date
from customer.models import Customer
from data_collector.models import Invoice
from data_engine_api.models import CustomerRevenue
from data_engine_api.calculator import advance, expected_fee, total_calculation, customer_total_calculation, source_customer_total_calculation

class CalculatorTest(TestCase):
    