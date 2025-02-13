from rest_framework import serializers
from .models import Product, ProductImage
from category.models import Category
from django.utils.text import slugify


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    product_images = serializers.ListField(
        child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True,
        required=False
    )
    product_category = serializers.CharField(write_only=True)
    product_sub_category = serializers.CharField(write_only=True)
    product_name = serializers.CharField(source='title')
    product_price = serializers.DecimalField(source='price', max_digits=10, decimal_places=2)
    product_description = serializers.CharField(source='description')
    product_location = serializers.CharField(write_only=True)
    product_condition = serializers.CharField(write_only=True)
    product_brand = serializers.CharField(write_only=True)
    product_promotion = serializers.CharField(write_only=True, required=False)
    product_seller = serializers.CharField(source='seller', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'product_name', 'slug', 'product_description', 
            'product_price', 'product_category', 'product_sub_category',
            'product_location', 'product_condition', 'product_brand', 'product_seller',
            'product_promotion', 'images', 'product_images',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Extract image data
        images = validated_data.pop('product_images', [])
        
        # Extract category data
        category_name = validated_data.pop('product_category')
        subcategory_name = validated_data.pop('product_sub_category')
        
        try:
            # Get category by name
            category = Category.objects.get(name=subcategory_name)
        except Category.DoesNotExist:
            raise serializers.ValidationError({"error": "Category not found"})

        # Prepare product data
        product_data = {
            'title': validated_data.get('title'),
            'description': validated_data.get('description'),
            'price': validated_data.get('price'),
            'category': category,
            'seller': self.context['request'].user,
            'contact_email': self.context['request'].user.email,
            'slug': slugify(validated_data.get('title')),
            # Add other fields as needed
        }

        # Create product
        product = Product.objects.create(**product_data)

        # Create product images
        for index, image in enumerate(images):
            ProductImage.objects.create(
                product=product,
                image=image,
                is_primary=(index == 0)  # First image is primary
            )

        return product


# class ProductImageSerializer(serializers.ModelSerializer):
#     image_url = serializers.SerializerMethodField()

#     class Meta:
#         model = ProductImage
#         fields = ['id', 'image', 'is_primary', 'created_at', 'image_url']

#     def get_image_url(self, obj):
#         request = self.context.get('request')
#         if obj.image and hasattr(obj.image, 'url'):
#             return request.build_absolute_uri(obj.image.url) if request else obj.image.url
#         return None

# class ProductSerializer(serializers.ModelSerializer):
#     images = ProductImageSerializer(many=True, read_only=True)
#     uploaded_images = serializers.ListField(
#         child=serializers.ImageField(max_length=1000000, allow_empty_file=False, use_url=False),
#         write_only=True,
#         required=False
#     )
#     category_path = serializers.SerializerMethodField()
#     primary_image_url = serializers.SerializerMethodField()
#     seller_name = serializers.SerializerMethodField()

#     class Meta:
#         model = Product
#         fields = [
#             'id', 'title', 'slug', 'description', 'price',
#             'category', 'category_path', 'seller', 'seller_name',
#             'is_active', 'contact_email', 'contact_phone',
#             'created_at', 'updated_at', 'images', 'uploaded_images',
#             'primary_image_url'
#         ]
#         read_only_fields = ['seller', 'slug', 'category_path']

#     def get_category_path(self, obj):
#         return [
#             CategorySerializer(category).data 
#             for category in obj.all_categories
#         ]

#     def get_primary_image_url(self, obj):
#         request = self.context.get('request')
#         primary_image = obj.primary_image
#         if primary_image and hasattr(primary_image.image, 'url'):
#             return request.build_absolute_uri(primary_image.image.url) if request else primary_image.image.url
#         return None

#     def get_seller_name(self, obj):
#         return obj.seller.get_full_name() or obj.seller.username

#     def create(self, validated_data):
#         uploaded_images = validated_data.pop('uploaded_images', [])
#         product = Product.objects.create(**validated_data)
        
#         for index, image in enumerate(uploaded_images):
#             ProductImage.objects.create(
#                 product=product,
#                 image=image,
#                 is_primary=(index == 0)  # First image is primary
#             )
        
#         return product

#     def update(self, instance, validated_data):
#         uploaded_images = validated_data.pop('uploaded_images', [])
        
#         # Update product fields
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         instance.save()
        
#         # Handle new images
#         if uploaded_images:
#             existing_images = instance.images.exists()
#             for index, image in enumerate(uploaded_images):
#                 ProductImage.objects.create(
#                     product=instance,
#                     image=image,
#                     is_primary=(not existing_images and index == 0)  # Make primary only if no existing images
#                 )
        
#         return instance