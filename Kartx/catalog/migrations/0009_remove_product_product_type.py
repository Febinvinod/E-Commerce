# Generated by Django 5.1.4 on 2025-01-09 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0008_product_approved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='product_type',
        ),
    ]
