from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from data_collector.forms import ExcelUploadForm
from data_collector.models import Invoice, InvoiceFile
from datetime import date
from decimal import Decimal
import os

class ExcelUploadFormTest(TestCase):
    def test_valid_csv_upload(self):
        # Create a sample CSV file content
        csv_content = "date,invoice number,value,haircut percent,Daily fee percent,currency,Revenue source,customer,Expected payment duration\n"
        csv_content += "2022-01-01,123,100.00,0.05,0.002,USD,Product A,John Doe,30\n"

        # Create a SimpleUploadedFile with the CSV content
        csv_file = SimpleUploadedFile("file.csv", csv_content.encode("utf-8"))

        # Create form data with the CSV file
        form_data = {'title': 'test','file': csv_file}
        form = ExcelUploadForm(data=form_data, files=form_data)

        # Check if the form is valid
        self.assertTrue(form.is_valid())


    def test_invalid_file_extension(self):
        # Create a sample non-CSV file content
        text_content = "This is not a CSV file."

        # Create a SimpleUploadedFile with the text content and a non-CSV extension
        text_file = SimpleUploadedFile("file.txt", text_content.encode("utf-8"))

        # Create form data with the non-CSV file
        form_data = {'title': 'test', 'file': text_file}
        form = ExcelUploadForm(data=form_data, files=form_data)

        # Check if the form is invalid due to an incorrect file extension
        self.assertFalse(form.is_valid())
        self.assertIn("Only CSV files are allowed.", form.errors['file'][0])

    def test_invalid_csv_headers(self):
        # Create a sample CSV file content with invalid headers
        csv_content = "date,invalid_column1,invalid_column2\n"
        csv_content += "2022-01-01,123,100.00\n"

        # Create a SimpleUploadedFile with the CSV content
        csv_file = SimpleUploadedFile("file.csv", csv_content.encode("utf-8"))

        # Create form data with the CSV file
        form_data = {'title': 'test', 'file': csv_file}
        form = ExcelUploadForm(data=form_data, files=form_data)

        # Check if the form is invalid due to incorrect headers
        self.assertFalse(form.is_valid())
        self.assertIn("Invalid header. Expected", form.errors['file'][0])


class ProcessFileDataToDbTest(TestCase):

    # All data from excel file is correct and is correctly stored
    def test_process_file_data_to_db(self):
        # Create a test CSV file content
        csv_content = "date,invoice number,value,haircut percent,Daily fee percent,currency,Revenue source,customer,Expected payment duration\n"
        csv_content += "2022-01-01,123,100.00,0.05,0.002,USD,Product A,Test Customer,30\n"

        # Create a SimpleUploadedFile with the CSV content
        csv_file = SimpleUploadedFile("file.csv", csv_content.encode("utf-8"))

        # Create an InvoiceFile object
        invoice_file = InvoiceFile.objects.create(file=csv_file, title='test 1')
        # The signal when creating InvoiceFile calls the function process_file_data_to_db
        # Check if Invoice objects are created in the database
        invoices = Invoice.objects.all()
         # Removing file from system
        try:
            os.remove(invoice_file.file.path)
        except:
            pass
        self.assertEqual(len(invoices), 1)

        # Check the details of the created invoice
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

    # There's a repeated row in the spreadsheet with the same customer and invoice number, and only creates invoice for the first one
    def test_process_file_data_to_db_repeated_row(self):
        # Create a test CSV file content
        csv_content = "date,invoice number,value,haircut percent,Daily fee percent,currency,Revenue source,customer,Expected payment duration\n"
        csv_content += "2022-01-01,123,100.00,0.05,0.002,USD,Product A,Test Customer,30\n"
        csv_content += "2022-01-01,123,90.00,0.05,0.002,USD,Product A,Test Customer,30\n"

        # Create a SimpleUploadedFile with the CSV content
        csv_file = SimpleUploadedFile("file.csv", csv_content.encode("utf-8"))

        # Create an InvoiceFile object
        invoice_file = InvoiceFile.objects.create(file=csv_file, title='test 1')
        # The signal when creating InvoiceFile calls the function process_file_data_to_db
        # Check if Invoice objects are created in the database
        invoices = Invoice.objects.all()
        # Removing file from system
        try:
            os.remove(invoice_file.file.path)
        except:
            pass
        self.assertEqual(len(invoices), 1)

        # Check the details of the created invoice
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

    # Same invoice number but different customer. Creates both entries
    def test_process_file_data_to_db_repeated_invoice(self):
        # Create a test CSV file content
        csv_content = "date,invoice number,value,haircut percent,Daily fee percent,currency,Revenue source,customer,Expected payment duration\n"
        csv_content += "2022-01-01,123,100.00,0.05,0.002,USD,Product A,Test Customer,30\n"
        csv_content += "2022-01-01,123,90.00,0.05,0.002,USD,Product A,Test Customer 2,30\n"

        # Create a SimpleUploadedFile with the CSV content
        csv_file = SimpleUploadedFile("file.csv", csv_content.encode("utf-8"))

        # Create an InvoiceFile object
        invoice_file = InvoiceFile.objects.create(file=csv_file, title='test 1')
        # The signal when creating InvoiceFile calls the function process_file_data_to_db
        # Check if Invoice objects are created in the database
        invoices = Invoice.objects.all()
         # Removing file from system
        try:
            os.remove(invoice_file.file.path)
        except:
            pass
        self.assertEqual(len(invoices), 2)

        # Check the details of the created invoice
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

    # Invalid value of invoice number, does not create the invoice
    def test_process_file_data_to_db_invalid_invoice(self):
        # Create a test CSV file content
        csv_content = "date,invoice number,value,haircut percent,Daily fee percent,currency,Revenue source,customer,Expected payment duration\n"
        csv_content += "2022-01-01,0,90.00,0.05,0.002,USD,Product A,Test Customer,30\n"

        # Create a SimpleUploadedFile with the CSV content
        csv_file = SimpleUploadedFile("file.csv", csv_content.encode("utf-8"))

        # Create an InvoiceFile object
        invoice_file = InvoiceFile.objects.create(file=csv_file, title='test 1')
        # The signal when creating InvoiceFile calls the function process_file_data_to_db
        # Check if Invoice objects are created in the database
        invoices = Invoice.objects.all()
         # Removing file from system
        try:
            os.remove(invoice_file.file.path)
        except:
            pass
        self.assertEqual(len(invoices), 0)

    # Different 0's around the values, creates the invoices 
    def test_process_file_data_to_db_value_zero(self):
        # Create a test CSV file content
        csv_content = "date,invoice number,value,haircut percent,Daily fee percent,currency,Revenue source,customer,Expected payment duration\n"
        csv_content += "2022-01-01,123,0,0.05,0.002,USD,Product A,Test Customer,30\n"
        csv_content += "2022-01-01,124,90.00,0,0.002,USD,Product A,Test Customer,30\n"
        csv_content += "2022-01-01,125,90.00,0.05,0,USD,Product A,Test Customer,30\n"
        csv_content += "2022-01-01,126,90.00,0.05,0.002,USD,Product A,Test Customer,0\n"


        # Create a SimpleUploadedFile with the CSV content
        csv_file = SimpleUploadedFile("file.csv", csv_content.encode("utf-8"))


        # Create an InvoiceFile object
        invoice_file = InvoiceFile.objects.create(file=csv_file, title='test 1')
        # The signal when creating InvoiceFile calls the function process_file_data_to_db
        # Check if Invoice objects are created in the database
        invoices = Invoice.objects.all()
         # Removing file from system
        try:
            os.remove(invoice_file.file.path)
        except:
            pass
        self.assertEqual(len(invoices), 4)

