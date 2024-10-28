from django.db import models

# Create your models here.
class SubCategory(models.Model):
    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey('category.Category', on_delete=models.CASCADE, related_name='subcategories')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Sub Categories"
