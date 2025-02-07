from django.db import models
from category.models import Category
from userauth.models import CustomUser
from django.core.exceptions import ValidationError

class ProductAttribute(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='attributes', 
                                on_delete=models.CASCADE)
    FIELD_TYPES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('boolean', 'Yes/No'),
        ('choice', 'Multiple Choice'),
        ('date', 'Date'),
    ]
    field_type = models.CharField(max_length=20, choices=FIELD_TYPES)
    is_required = models.BooleanField(default=False)
    choices = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        ordering = ['name']
        unique_together = ['category', 'name']
    
    def __str__(self):
        return f"{self.category.full_path} - {self.name}"

class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', 
                                on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, related_name='products', 
                              on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def clean(self):
        if self.category and self.category.subcategories.exists():
            raise ValidationError(
                'Products can only be created in leaf categories.'
            )

class ProductAttributeValue(models.Model):
    product = models.ForeignKey(Product, related_name='attribute_values', 
                               on_delete=models.CASCADE)
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    value = models.JSONField()
    
    class Meta:
        unique_together = ('product', 'attribute')