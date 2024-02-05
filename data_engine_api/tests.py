from django.test import TestCase
from decimal import Decimal
from datetime import date
from customer.models import Customer
from data_collector.models import Invoice
from data_engine_api.models import CustomerRevenue
from data_engine_api.calculator import advance, expected_fee, total_calculation, customer_total_calculation, source_customer_total_calculation

class CalculatorTest(TestCase):
    def setUp(self):
        # Create a test customer
        self.test_customer = Customer.objects.create(name='Test Customer')

        # Create test invoices
        self.invoice1 = Invoice.objects.create(
            date=date(2022, 1, 1),
            invoice_number='INV001',
            value=Decimal('100.00'),
            haircut_percent=Decimal('10.0'),
            daily_fee_percent=Decimal('5.0'),
            currency='USD',
            revenue_source='Source A',
            customer=self.test_customer,
            expected_payment_duration=30
        )

        self.invoice1_advance = Decimal('90.00')

        self.invoice2 = Invoice.objects.create(
            date=date(2022, 1, 2),
            invoice_number='INV002',
            value=Decimal('150.00'),
            haircut_percent=Decimal('15.0'),
            daily_fee_percent=Decimal('7.0'),
            currency='GBP',
            revenue_source='Source B',
            customer=self.test_customer,
            expected_payment_duration=45
        )

        self.invoice2_advance = Decimal('165.00')

        self.revenue = CustomerRevenue(
            customer=self.test_customer,
            revenue_source='Source A',
            value=Decimal('100.00') + Decimal('150.00'),
            advance=Decimal('90.00') + advance(Decimal('150.00'), Decimal('15.0')),
            expected_fee=expected_fee(Decimal('90.00'), Decimal('5.0')) + expected_fee(advance(Decimal('150.00'), Decimal('15.0')), Decimal('7.0'))
        )

    def test_advance_calculation(self):
        # Test advance calculation
        calculated_advance = advance(self.invoice1.value, self.invoice1.haircut_percent)
        self.assertEqual(calculated_advance, self.invoice1_advance)

    def test_expected_fee_calculation(self):
        # Test expected fee calculation
        invoice_advance = advance(self.invoice2.value, self.invoice2.haircut_percent)
        calculated_fee = expected_fee(invoice_advance, self.invoice2.daily_fee_percent)
        expected_fee_value = Decimal('9.45')  # Expected value based on the provided formula
        self.assertEqual(calculated_fee, self.invoice2_expected_fee)

    def test_source_customer_total_calculation(self):
        # Test source customer total calculation
        calculated_customer_revenue = source_customer_total_calculation(
            self.test_customer, Invoice.objects.all(), ['Source A', 'Source B']
        )
        expected_customer_revenue = 
        self.assertEqual(calculated_customer_revenue, expected_customer_revenue)

    def test_customer_total_calculation(self):
        # Test customer total calculation
        customer_total_calculation(self.test_customer)
        customer_revenue = CustomerRevenue.objects.get(customer=self.test_customer, revenue_source='Source A')
        self.assertEqual(customer_revenue.value, Decimal('100.00') + Decimal('150.00'))
        # Add more assertions as needed

    def test_total_calculation(self):
        # Test total calculation
        total_calculation()
        # Add assertions to check the results after total calculation
        customer_revenue_source_a = CustomerRevenue.objects.get(customer=self.test_customer, revenue_source='Source A')
        customer_revenue_source_b = CustomerRevenue.objects.get(customer=self.test_customer, revenue_source='Source B')

        self.assertEqual(customer_revenue_source_a.value, Decimal('100.00'))
        self.assertEqual(customer_revenue_source_b.value, Decimal('150.00'))

