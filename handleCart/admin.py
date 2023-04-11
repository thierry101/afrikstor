from django.contrib import admin

from handleCart.models import Order, OrderItem, CouponGerate, ShippingAdress

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(CouponGerate)
admin.site.register(ShippingAdress)
