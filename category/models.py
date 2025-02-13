from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, 
                              related_name='subcategories', 
                              on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, null=True, blank=True)
    level = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "categories"
        ordering = ['name']
    
    def __str__(self):
        if self.parent:
            return f"{self.parent.name} → {self.name}"
        return self.name
    
    def save(self, *args, **kwargs):
        if self.parent:
            self.level = self.parent.level + 1
        super().save(*args, **kwargs)
    
    @property
    def full_path(self):
        if self.parent:
            return f"{self.parent.full_path}/{self.name}"
        return self.name

    def get_all_subcategories(self):
        """
        Recursively get all subcategories of this category
        """
        subcategories = list(self.subcategories.all())
        for subcategory in self.subcategories.all():
            subcategories.extend(subcategory.get_all_subcategories())
        return subcategories