from .models import Product, ProductAttribute
from .serializers import ProductSerializer, ProductAttributeSerializer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class ProductAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
    # permission_classes = [IsAuthenticated]
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['category', 'field_type', 'is_required']

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly, IsSellerOrReadOnly]
    # filter_backends = [DjangoFilterBackend, filters.SearchFilter, 
    #                   filters.OrderingFilter]
    # filterset_class = ProductFilter
    # search_fields = ['title', 'description']
    # ordering_fields = ['created_at', 'price']
    # lookup_field = 'slug'
    
    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)
    
    @action(detail=False)
    def my_products(self, request):
        products = self.get_queryset().filter(seller=request.user)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)