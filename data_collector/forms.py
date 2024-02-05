from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings
#from django.contrib import messages
from .models import InvoiceFile
import pandas as pd
import io

class ExcelUploadForm(forms.ModelForm):
    class Meta:
        model = InvoiceFile
        fields = '__all__'

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']

        # Only allowing csv spreadsheets for simplicity
        if not uploaded_file.name.lower().endswith('.csv'):
            raise ValidationError("Only CSV files are allowed.")

        file_content = uploaded_file.read()

        # Creating a temporary copy of the file in memory, ensuring that the file content
        # can be read by pandas.read_csv without affecting the following file save.
        csv_file = io.BytesIO(file_content)

        # Read the CSV file using pandas
        df = pd.read_csv(csv_file)

        # Expected headers
        expected_headers = settings.EXCEL_HEADERS
        # Check if the headers match the expected headers
        headers = []
        for header in expected_headers:
            if header not in list(df.columns):
                headers.append(header)
        if headers:
            raise ValidationError(f"Invalid header. missing header:{','.join(headers)}.")

        # Data validation:
        # We check if there's any data duplicates "invoice number - customer"
        if df.duplicated(subset=['invoice number','customer']).any():
            # messages.add_message(self.re, messages.INFO, 'Duplicated values')
            pass
        conditions = (df['invoice number'] <= 0) & (df['value'] < 0) & (df['haircut percent'] < 0) & (df['Daily fee percent'] < 0) & (df['Expected payment duration'] < 0)
        if conditions.any():
            #TODO: send warning
            pass
        # If headers match, return the original uploaded_file
        return uploaded_file
