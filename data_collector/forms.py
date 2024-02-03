# forms.py

from django import forms
from django.core.exceptions import ValidationError
from .models import InvoiceFile
import pandas as pd
import io

class ExcelUploadForm(forms.ModelForm):
    class Meta:
        model = InvoiceFile
        fields = '__all__'

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']

        # Validate file extension
        if not uploaded_file.name.lower().endswith('.csv'):
            raise ValidationError("Only CSV files are allowed.")
        
        file_content = uploaded_file.read()
        csv_file = io.BytesIO(file_content)

        # Read the CSV file using pandas
        df = pd.read_csv(csv_file)

        # Expected headers
        expected_headers = ['date', 'invoice number', 'value', 'haircut percent', 'Daily fee percent', 'currency', 'Revenue source', 'customer', 'Expected payment duration']

        # Check if the headers match the expected headers
        actual_headers = list(df.columns)
        if expected_headers != actual_headers:
            raise ValidationError(f"Invalid header. Expected {expected_headers}, but found {actual_headers}.")
        
        # If headers match, return the original uploaded_file
        return uploaded_file
