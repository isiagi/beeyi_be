from django.db import models
from category.models import Category
from userauth.models import CustomUser
from django.core.exceptions import ValidationError

class ProductImage(models.Model):
    product = models.ForeignKey('Product', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/%Y/%m/%d/')
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_primary', '-created_at']

    def __str__(self):
        return f"Image for {self.product.title}"

    def save(self, *args, **kwargs):
        if self.is_primary:
            # Set all other images of this product to not primary
            ProductImage.objects.filter(product=self.product, is_primary=True).update(is_primary=False)
        super().save(*args, **kwargs)

class Product(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, related_name='products', 
                                on_delete=models.CASCADE)
    seller = models.ForeignKey(CustomUser, related_name='products', 
                              on_delete=models.CASCADE)
    condition = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

    @property
    def primary_image(self):
        return self.images.filter(is_primary=True).first()

    @property
    def all_categories(self):
        """
        Returns a list of all parent categories including the product's direct category
        """
        categories = []
        current_category = self.category
        while current_category:
            categories.append(current_category)
            current_category = current_category.parent
        return categories[::-1]  # Reverse to get root -> leaf order