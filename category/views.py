from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
# from rest_framework import filters
from .serializer import RecursiveCategorySerializer
from .models import Category
from .serializer import CategorySerializer
from django.shortcuts import get_object_or_404

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # lookup_field = 'slug'
    # filter_backends = [filters.SearchFilter]
    # search_fields = ['name', 'description']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return RecursiveCategorySerializer
        return CategorySerializer
    
    @action(detail=True)
    def attributes(self, request, slug=None):
        category = self.get_object()
        # Get attributes from current category and all parent categories
        attributes = ProductAttribute.objects.none()
        current_category = category
        while current_category:
            attributes |= current_category.attributes.all()
            current_category = current_category.parent
        
        serializer = ProductAttributeSerializer(attributes, many=True)
        return Response(serializer.data)
    
    @action(detail=True)
    def products(self, request, slug=None):
        category = self.get_object()
        products = Product.objects.filter(
            category=category,
            # is_active=True
        )
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='subcategories/(?P<slug>[^/.]+)')
    def subcategories(self, request, slug=None):
        """
        Retrieve all subcategories of a given category (recursively) using slug.
        """
        category = get_object_or_404(Category, slug=slug)
        subcategories = category.get_all_subcategories()
        serializer = CategorySerializer(subcategories, many=True)
        return Response(serializer.data)
