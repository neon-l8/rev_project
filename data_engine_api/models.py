from django.db import models

class CustomerRevenue(models.Model):
    customer = models.ForeignKey('customer.Customer', on_delete=models.CASCADE)
    revenue_source = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    advance = models.DecimalField(max_digits=10, decimal_places=2)
    expected_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.customer} - {self.revenue_source}"

    class Meta:
        unique_together = ('customer', 'revenue_source')
        verbose_name_plural = "Customer Revenues"

