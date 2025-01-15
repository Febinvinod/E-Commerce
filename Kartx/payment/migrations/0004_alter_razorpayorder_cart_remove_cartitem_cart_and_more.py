# Generated by Django 5.1.4 on 2025-01-15 05:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kartx_cart', '0003_alter_cartitem_cart'),
        ('payment', '0003_rename_status_razorpayorder_payment_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='razorpayorder',
            name='cart',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='kartx_cart.cart'),
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
