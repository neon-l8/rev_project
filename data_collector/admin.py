from django.contrib import admin
from .models import InvoiceFile, Invoice
from .forms import ExcelUploadForm

class InvoiceFileAdmin(admin.ModelAdmin):
    form = ExcelUploadForm

admin.site.register(InvoiceFile ,InvoiceFileAdmin)
admin.site.register(Invoice)
