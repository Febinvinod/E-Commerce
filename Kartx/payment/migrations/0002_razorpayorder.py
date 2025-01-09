# Generated by Django 5.1.4 on 2025-01-09 05:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RazorpayOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=255, unique=True)),
                ('payment_id', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(default='created', max_length=50)),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='razorpay_order', to='payment.cart')),
            ],
        ),
    ]