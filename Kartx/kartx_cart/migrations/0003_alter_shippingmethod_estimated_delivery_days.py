# Generated by Django 5.1.4 on 2025-01-08 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kartx_cart', '0002_shippingmethod_address_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shippingmethod',
            name='estimated_delivery_days',
            field=models.IntegerField(null=True),
        ),
    ]
