from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Cart,CartItem,Address,ShippingMethod,Order

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Address)
admin.site.register(ShippingMethod)
admin.site.register(Order)