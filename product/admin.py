from django.contrib import admin
from .models import Product, ProductAttribute, ProductAttributeValue

# Register your models here.

admin.site.register(Product)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeValue)

