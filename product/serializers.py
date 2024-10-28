from rest_framework import serializers
from .models import Product
from category.models import Category
from subcategory.models import SubCategory

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    sub_category = serializers.PrimaryKeyRelatedField(queryset=SubCategory.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'condition', 'sub_category', 'images','created_at', 'updated_at']

class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    sub_category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category', 'sub_category', 'images','description', 'condition']

class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    sub_category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'condition', 'category', 'images', 'sub_category', 'created_at', 'updated_at']
