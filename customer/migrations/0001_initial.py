# Generated by Django 4.2 on 2024-02-03 14:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerRevenue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('revenue_source', models.CharField(max_length=255)),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('advance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('expected_fee', models.DecimalField(decimal_places=2, max_digits=10)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.customer')),
            ],
            options={
                'verbose_name_plural': 'Customer Revenues',
                'unique_together': {('customer', 'revenue_source')},
            },
        ),
    ]
