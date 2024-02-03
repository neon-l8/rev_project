from django.contrib import admin
from .models import InvoiceFile, Invoice

admin.site.register(InvoiceFile)
admin.site.register(Invoice)
