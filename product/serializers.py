from rest_framework import serializers
from .models import Product
from category.models import Category
from subcategory.models import SubCategory

class ProductSerializer(serializers.ModelSerializer):
    product_category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all() )
    product_sub_category = serializers.SlugRelatedField(slug_field='name', queryset=SubCategory.objects.all() )

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_description', 'product_price', 'product_category', 'product_condition', 'product_sub_category', 'product_image', 'product_brand', 'product_location','created_at', 'updated_at']

class ProductListSerializer(serializers.ModelSerializer):
    product_category = serializers.StringRelatedField()
    product_sub_category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_price', 'product_category', 'product_sub_category', 'product_image','product_description', 'product_condition']

class ProductDetailSerializer(serializers.ModelSerializer):
    product_category = serializers.StringRelatedField()
    product_sub_category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_description', 'product_price', 'product_condition', 'product_category', 'product_image', 'product_sub_category', 'created_at', 'updated_at']
