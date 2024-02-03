from django.db import models

class InvoiceFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='invoices/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Invoice(models.Model):
    date = models.DateField()
    invoice_number = models.CharField(max_length=50, unique=True)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    haircut_percent = models.DecimalField(max_digits=5, decimal_places=2)
    daily_fee_percent = models.DecimalField(max_digits=5, decimal_places=4)
    currency = models.CharField(max_length=3)
    revenue_source = models.CharField(max_length=255)
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)
    expected_payment_duration = models.PositiveIntegerField()

    def __str__(self):
        return f"Invoice #{self.invoice_number} - {self.customer}"
