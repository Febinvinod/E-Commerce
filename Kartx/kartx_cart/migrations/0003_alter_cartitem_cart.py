# Generated by Django 5.1.4 on 2025-01-15 05:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kartx_cart', '0002_cart_user_cartitem_visible_alter_cartitem_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='kartx_cart.cart'),
        ),
    ]