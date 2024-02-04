import pandas as pd
from django.conf import settings
from customer.models import Customer
from data_collector.models import Invoice
from itertools import islice


def process_file_data_to_db(invoice_file):
    csv_file = invoice_file.file
    # Read the CSV file using Pandas DataFrame
    expected_headers = settings.EXCEL_HEADERS
    df = pd.read_csv(csv_file, names=expected_headers, skiprows=1)  # Skip the first row since it contains header names

    # Convert 'date' column to datetime format
    df['date'] = pd.to_datetime(df['date'], errors='coerce', yearfirst=True)

    # We create the customers if they don't exist
    df['customer'] = df['customer'].apply(lambda customer_name: Customer.objects.get_or_create(name=customer_name)[0].id)

    # Filter out rows with specified conditions
    df = df[(df['value'] != 0) & (df['haircut percent'] != 0) & (df['Daily fee percent'] != 0) & (df['Expected payment duration'] != 0)]

    # Deduplicate based on 'invoice_number' and keep the first occurrence
    df = df.drop_duplicates(subset='invoice number', keep='first')

    # Create Invoice objects from DataFrame rows
    invoices = []
    for index, row in df.iterrows():
        invoice = Invoice(
            date=row['date'],
            invoice_number=row['invoice number'],
            value=row['value'],
            haircut_percent=row['haircut percent'],
            daily_fee_percent=row['Daily fee percent'],
            currency=row['currency'],
            revenue_source=row['Revenue source'],
            customer_id=row['customer'],
            expected_payment_duration=row['Expected payment duration'],
        )
        invoices.append(invoice)

    # Create objects in bulk create to reduce queries to db
    Invoice.objects.bulk_create(invoices)

    return len(invoices)  # Optional: Return the number of created invoices
