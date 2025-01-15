# Generated by Django 5.1.4 on 2025-01-15 06:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('kartx_cart', '0003_alter_cartitem_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='RazorpayOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=255, unique=True)),
                ('payment_id', models.CharField(blank=True, max_length=255, null=True)),
                ('payment_status', models.CharField(choices=[('created', 'Created'), ('paid', 'Paid'), ('failed', 'Failed'), ('refunded', 'Refunded')], default='created', max_length=50)),
                ('payment_date', models.DateTimeField(blank=True, null=True)),
                ('amount_paid', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('transaction_id', models.CharField(blank=True, max_length=255, null=True)),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='kartx_cart.cart')),
            ],
        ),
    ]
