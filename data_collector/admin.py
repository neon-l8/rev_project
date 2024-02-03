from django.contrib import admin

# Register your models here.
# admin.py

from .models import InvoiceFile

admin.site.register(InvoiceFile)
