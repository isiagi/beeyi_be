from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Product, ProductImage
from .serializers import ProductSerializer, ProductImageSerializer
from category.models import Category


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category', None)
        search = self.request.query_params.get('search', None)
        
        if category:
            category_obj = None
            
            # Try different ways to match the category
            try:
                # First try to get category by ID
                category_id = int(category)
                category_obj = Category.objects.get(id=category_id)
            except (ValueError, Category.DoesNotExist):
                # Then try slug or name (case-insensitive)
                category_obj = Category.objects.filter(
                    Q(slug=category) |
                    Q(name__iexact=category)
                ).first()
            
            if category_obj:
                # Get the category and all its subcategories
                subcategories = [category_obj] + category_obj.get_all_subcategories()
                queryset = queryset.filter(category__in=subcategories)
            else:
                # If no exact match found, try partial match on category names
                matching_categories = Category.objects.filter(
                    name__icontains=category
                )
                if matching_categories.exists():
                    all_subcategories = []
                    for cat in matching_categories:
                        all_subcategories.extend([cat] + cat.get_all_subcategories())
                    queryset = queryset.filter(category__in=all_subcategories)
                else:
                    return Product.objects.none()

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )

        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    @action(detail=True, methods=['post'])
    def upload_images(self, request, *args, **kwargs):
        product = self.get_object()
        images = request.FILES.getlist('product_images')
        
        if not images:
            return Response(
                {'error': 'No images provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        created_images = []
        for index, image in enumerate(images):
            product_image = ProductImage.objects.create(
                product=product,
                image=image,
                is_primary=(not product.images.exists() and index == 0)
            )
            created_images.append(product_image)
        
        serializer = ProductImageSerializer(created_images, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['delete'])
    def delete_image(self, request, *args, **kwargs):
        product = self.get_object()
        image_id = request.data.get('image_id')
        
        try:
            image = product.images.get(id=image_id)
            was_primary = image.is_primary
            image.delete()
            
            # If we deleted the primary image, set the first remaining image as primary
            if was_primary:
                first_image = product.images.first()
                if first_image:
                    first_image.is_primary = True
                    first_image.save()
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ProductImage.DoesNotExist:
            return Response(
                {'error': 'Image not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        

    # Get products of current user
    @action(detail=False, methods=['get'])
    def my_products(self, request):
        user = request.user
        products = Product.objects.filter(seller=user)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)