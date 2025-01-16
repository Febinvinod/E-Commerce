# Generated by Django 5.1.4 on 2025-01-16 07:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kartx_cart', '0003_alter_cartitem_cart'),
        ('payment', '0003_paymentnew_delete_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentSuccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=255)),
                ('payment_status', models.CharField(default='paid', max_length=20)),
                ('cart_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='kartx_cart.cart')),
            ],
        ),
    ]
