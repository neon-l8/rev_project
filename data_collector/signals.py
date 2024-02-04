from django.dispatch import receiver
from django.db.models.signals import post_save
from data_collector.utils import process_file_data_to_db
from data_collector.models import InvoiceFile

@receiver(post_save, sender=InvoiceFile)
def on_invoice_file_save(sender, instance, **kwargs):
    process_file_data_to_db(instance)