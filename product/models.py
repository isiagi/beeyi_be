from django.db import models
from category.models import Category
from subcategory.models import SubCategory


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class Product(models.Model):
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
        ('refurbished', 'Refurbished'),
    ]

    product_name = models.CharField(max_length=200)
    product_description = models.TextField()
    product_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_location = models.CharField(max_length=200)
    product_brands = models.CharField(max_length=150) 
    product_image = models.ImageField(upload_to=upload_to, blank=True, null=True) # Store an array of image URLs
    product_condition = models.CharField(max_length=20, choices=CONDITION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name


