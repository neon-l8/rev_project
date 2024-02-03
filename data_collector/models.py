from django.db import models

class InvoiceFile(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
""" 
class Invoice(models.Model):
    date	
    invoice number	
    value	
    haircut percent	
    Daily fee percent	
    currency	
    Revenue source	
    customer	
    Expected payment duration
     """