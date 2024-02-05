from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from data_collector.forms import ExcelUploadForm
from data_collector.models import Invoice, InvoiceFile
from datetime import date
from decimal import Decimal
import os

class ProcessFileDataToDbTest(TestCase):

    # Test that validates that when there are two repeated rows (matches with customer and invoice number)
    # only creates invoice for the first one
    def test_process_file_data_to_db_repeated_row(self):
        csv_content = "date,invoice number,value,haircut percent,Daily fee percent,currency,Revenue source,customer,Expected payment duration\n"
        csv_content += "2022-01-01,123,100.00,0.05,0.002,USD,Product A,Test Customer,30\n"
        csv_content += "2022-01-01,123,90.00,0.05,0.002,USD,Product A,Test Customer,30\n"

        csv_file = SimpleUploadedFile("file.csv", csv_content.encode("utf-8"))

        invoice_file = InvoiceFile.objects.create(file=csv_file, title='test 1')
        # The signal when creating InvoiceFile calls the function process_file_data_to_db
        # Check that only the first object is created
        invoices = Invoice.objects.all()
        # Removing file from system
        try:
            os.remove(invoice_file.file.path)
        except:
            pass
        self.assertEqual(len(invoices), 1)

        # Check data to confirm that the added Invoice is the first one
        created_invoice = invoices[0]
        self.assertEqual(created_invoice.value, Decimal(100.00))

    # Test that validates when two invoices share invoice number but different customer
    def test_process_file_data_to_db_repeated_invoice(self):
        csv_content = "date,invoice number,value,haircut percent,Daily fee percent,currency,Revenue source,customer,Expected payment duration\n"
        csv_content += "2022-01-01,123,100.00,0.05,0.002,USD,Product A,Test Customer,30\n"
        csv_content += "2022-01-01,123,90.00,0.05,0.002,USD,Product A,Test Customer 2,30\n"

        csv_file = SimpleUploadedFile("file.csv", csv_content.encode("utf-8"))
        invoice_file = InvoiceFile.objects.create(file=csv_file, title='test 1')

        # Check if Invoice objects are created in the database
        invoices = Invoice.objects.all()
         # Removing file from system
        try:
            os.remove(invoice_file.file.path)
        except:
            pass
        self.assertEqual(len(invoices), 2)

        # Check the details of the created invoices and the data and datatypes match 
        created_invoice = invoices[0]
        self.assertEqual(created_invoice.date, date(2022, 1, 1))
        self.assertEqual(created_invoice.invoice_number, '123')
        self.assertEqual(created_invoice.value, Decimal(100.00))
        self.assertEqual(created_invoice.haircut_percent, Decimal('0.05'))
        self.assertEqual(created_invoice.daily_fee_percent, Decimal('0.002'))
        self.assertEqual(created_invoice.currency, 'USD')
        self.assertEqual(created_invoice.revenue_source, 'Product A')
        self.assertEqual(created_invoice.customer.name, 'Test Customer')
        self.assertEqual(created_invoice.expected_payment_duration, 30)

        # Check the details of the created invoice
        created_invoice = invoices[1]
        self.assertEqual(created_invoice.date, date(2022, 1, 1))
        self.assertEqual(created_invoice.invoice_number, '123')
        self.assertEqual(created_invoice.value, Decimal(90.00))
        self.assertEqual(created_invoice.haircut_percent, Decimal('0.05'))
        self.assertEqual(created_invoice.daily_fee_percent, Decimal('0.002'))
        self.assertEqual(created_invoice.currency, 'USD')
        self.assertEqual(created_invoice.revenue_source, 'Product A')
        self.assertEqual(created_invoice.customer.name, 'Test Customer 2')
        self.assertEqual(created_invoice.expected_payment_duration, 30)

    # Test that validates that when the invoice number is invalid it does not create an Invoice
    def test_process_file_data_to_db_invalid_invoice(self):
        # Create a test CSV file content
        csv_content = "date,invoice number,value,haircut percent,Daily fee percent,currency,Revenue source,customer,Expected payment duration\n"
        csv_content += "2022-01-01,0,90.00,0.05,0.002,USD,Product A,Test Customer,30\n"

        # Create a SimpleUploadedFile with the CSV content
        csv_file = SimpleUploadedFile("file.csv", csv_content.encode("utf-8"))
        invoice_file = InvoiceFile.objects.create(file=csv_file, title='test 1')
        invoices = Invoice.objects.all()
        try:
            os.remove(invoice_file.file.path)
        except:
            pass
        self.assertEqual(len(invoices), 0)

    # Test that validates that when there's 0s in the different fields the program can still read it and store it in DB.
    def test_process_file_data_to_db_value_zero(self):
        csv_content = "date,invoice number,value,haircut percent,Daily fee percent,currency,Revenue source,customer,Expected payment duration\n"
        csv_content += "2022-01-01,123,0,0.05,0.002,USD,Product A,Test Customer,30\n"
        csv_content += "2022-01-01,124,90.00,0,0.002,USD,Product A,Test Customer,30\n"
        csv_content += "2022-01-01,125,90.00,0.05,0,USD,Product A,Test Customer,30\n"
        csv_content += "2022-01-01,126,90.00,0.05,0.002,USD,Product A,Test Customer,0\n"

        csv_file = SimpleUploadedFile("file.csv", csv_content.encode("utf-8"))

        invoice_file = InvoiceFile.objects.create(file=csv_file, title='test 1')
        invoices = Invoice.objects.all()
        try:
            os.remove(invoice_file.file.path)
        except:
            pass
        self.assertEqual(len(invoices), 4)

