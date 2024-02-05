from django.test import TestCase
from collections import namedtuple
from data_engine_api.calculator import advance, expected_fee, sum_values_for_invoices
from decimal import Decimal
import math

class CalculatorTest(TestCase):
    def setUp(self):
        # Invoice 'struct' with precalculated data to validate the calculus
        self.InvoiceStruct = namedtuple('Invoice', 'value haircut_percent advance daily_fee_percent expected_fee')
        self.invoice1 = self.InvoiceStruct(value=Decimal(100),
                                           haircut_percent = Decimal(10), 
                                           advance = Decimal(90),
                                           daily_fee_percent = Decimal(0.015),
                                           expected_fee = Decimal(0.0135))

        self.invoice2 = self.InvoiceStruct(value=Decimal(1000),
                                           haircut_percent = Decimal(10), 
                                           advance = Decimal(900),
                                           daily_fee_percent = Decimal(0.455),
                                           expected_fee = Decimal(4.095))

        self.expected_total_value, self.expected_total_advance, self.expected_total_fee = Decimal(1100), Decimal(990), Decimal(4.1035)

    # We use math.isclose due to Decimal precision being superior than the precision of the expected values
    def test_advance_calculation(self):
        calculated_advance = advance(self.invoice1.value, self.invoice1.haircut_percent)
        self.assertTrue(math.isclose(calculated_advance, self.invoice1.advance, abs_tol=0.01))

    def test_expected_fee_calculation(self):
        calculated_fee = expected_fee(self.invoice1.advance, self.invoice1.daily_fee_percent)
        self.assertTrue(math.isclose(calculated_fee, self.invoice1.expected_fee, abs_tol=0.01))

    def test_sum_values_for_invoices(self):
        invoice_list = [self.invoice1, self.invoice2]
        total_value, total_advance, total_fee = sum_values_for_invoices(invoice_list)
        self.assertTrue(math.isclose(total_value, self.expected_total_value, abs_tol=0.01))
        self.assertTrue(math.isclose(total_advance, self.expected_total_advance, abs_tol=0.01))
        self.assertTrue(math.isclose(total_fee, self.expected_total_fee, abs_tol=0.01))
