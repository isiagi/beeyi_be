from .models import Product, ProductAttribute, ProductAttributeValue
from rest_framework import serializers


class ProductAttributeSerializer(serializers.ModelSerializer):
    category_path = serializers.CharField(source='category.full_path', 
                                        read_only=True)
    
    class Meta:
        model = ProductAttribute
        fields = ['id', 'name', 'category', 'category_path', 
                 'field_type', 'is_required', 'choices', 'created_at']
        read_only_fields = ['created_at']

class ProductAttributeValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.name', 
                                         read_only=True)
    
    class Meta:
        model = ProductAttributeValue
        fields = ['attribute', 'attribute_name', 'value']

class ProductSerializer(serializers.ModelSerializer):
    attribute_values = ProductAttributeValueSerializer(many=True)
    category_path = serializers.CharField(source='category.full_path', 
                                        read_only=True)
    seller_username = serializers.CharField(source='seller.username', 
                                          read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'slug', 'description', 'price',
                 'category', 'category_path', 'seller', 'seller_username',
                 'contact_email', 'contact_phone',
                 'attribute_values', 'created_at', 'updated_at']
        read_only_fields = ['seller', 'slug', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        attribute_values_data = validated_data.pop('attribute_values')
        product = Product.objects.create(**validated_data)
        
        # Create attribute values
        for attr_value in attribute_values_data:
            ProductAttributeValue.objects.create(
                product=product,
                **attr_value
            )
        return product
    
    def update(self, instance, validated_data):
        if 'attribute_values' in validated_data:
            attribute_values_data = validated_data.pop('attribute_values')
            # Clear existing values
            instance.attribute_values.all().delete()
            # Create new values
            for attr_value in attribute_values_data:
                ProductAttributeValue.objects.create(
                    product=instance,
                    **attr_value
                )
        
        return super().update(instance, validated_data)