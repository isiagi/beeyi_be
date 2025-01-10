from rest_framework import serializers
from .models import Product
from category.models import Category
from subcategory.models import SubCategory

class ProductSerializer(serializers.ModelSerializer):
    product_category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    product_sub_category = serializers.SlugRelatedField(slug_field='name', queryset=SubCategory.objects.all())
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_description', 'product_price', 
                 'product_category', 'product_condition', 'product_sub_category', 
                 'product_image', 'image_url', 'product_brand', 'product_location',
                 'created_at', 'updated_at']

    def get_image_url(self, obj):
        if obj.product_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.product_image.url)
            return obj.product_image.url
        return None

class ProductListSerializer(serializers.ModelSerializer):
    product_category = serializers.StringRelatedField()
    product_sub_category = serializers.StringRelatedField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_price', 'product_category', 
                 'product_sub_category', 'image_url', 'product_description', 
                 'product_condition']

    def get_image_url(self, obj):
        if obj.product_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.product_image.url)
            return obj.product_image.url
        return None

class ProductDetailSerializer(serializers.ModelSerializer):
    product_category = serializers.StringRelatedField()
    product_sub_category = serializers.StringRelatedField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_description', 'product_price', 
                 'product_condition', 'product_category', 'image_url', 
                 'product_sub_category', 'created_at', 'updated_at']

    def get_image_url(self, obj):
        if obj.product_image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.product_image.url)
            return obj.product_image.url
        return None