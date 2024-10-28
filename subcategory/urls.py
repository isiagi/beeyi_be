from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SubCategoryViewSet

router = DefaultRouter()
router.register('subcategories', SubCategoryViewSet, basename='subcategory')

urlpatterns = [
    path('', include(router.urls)),
]
