from django.contrib import admin

from adminProduct.models import Category, Size, SubCategory, Brand

# Register your models here.

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Size)
admin.site.register(Brand)
