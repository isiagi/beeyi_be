from rest_framework import serializers
from .models import Category
from subcategory.serializers import SubCategorySerializer

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories']
