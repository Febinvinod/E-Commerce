# Generated by Django 5.1.4 on 2025-01-09 06:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '__first__'),
        ('kartx_cart', '0004_alter_cart_session_key'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='is_default',
        ),
        migrations.RemoveField(
            model_name='address',
            name='session_key',
        ),
        migrations.RemoveField(
            model_name='address',
            name='state',
        ),
        migrations.RemoveField(
            model_name='address',
            name='street',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='product_id',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='shippingmethod',
            name='estimated_delivery_days',
        ),
        migrations.AddField(
            model_name='address',
            name='address_line_1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='address',
            name='address_line_2',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='catalog.product'),
        ),
        migrations.AlterField(
            model_name='address',
            name='city',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='address',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cart',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='order',
            name='cart',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='kartx_cart.cart'),
        ),
        migrations.AlterField(
            model_name='shippingmethod',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]