from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import SubCategory
from .serializers import SubCategorySerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    permission_classes = [AllowAny]


    @action(detail=False, methods=['get'], url_path='by-category-name/(?P<category_name>[^/.]+)')
    def by_category_name(self, request, category_name=None):
        """
        Custom action to filter subcategories based on category name.
        """
        subcategories = SubCategory.objects.filter(category__name=category_name)
        # Extracting names from the subcategories
        names = [subcategory.name for subcategory in subcategories]
        return Response(names)