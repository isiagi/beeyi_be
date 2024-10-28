from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Product
from .serializers import ProductSerializer, ProductListSerializer, ProductDetailSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    permission_classes = [AllowAny]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductSerializer
    

