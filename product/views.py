from django.shortcuts import render
import logging
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Product
from .serializers import ProductSerializer, ProductListSerializer, ProductDetailSerializer
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

# Configure a logger
logger = logging.getLogger(__name__)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductSerializer

    def create(self, request, *args, **kwargs):
        # Log the raw request body
        # logger.info(f"Raw request body: {request.body}")
        
        # Log parsed data (works for JSON and form data)
        # logger.info(f"Request data: {request.data}")
        
        # Log files if any
        if request.FILES:
            logger.info(f"Request files: {request.FILES}")
            
        # Log query parameters
        logger.info(f"Query params: {request.query_params}")
        
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info(f"Update request body: {request.body}")
        logger.info(f"Update request data: {request.data}")
        return super().update(request, *args, **kwargs)