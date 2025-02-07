from rest_framework import serializers
from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    level = serializers.IntegerField(read_only=True)
    full_path = serializers.CharField(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'slug', 
                 'level', 'full_path', 'created_at']
        read_only_fields = ['level', 'created_at']

class RecursiveCategorySerializer(CategorySerializer):
    subcategories = serializers.SerializerMethodField()
    
    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ['subcategories']
    
    def get_subcategories(self, obj):
        if obj.subcategories.exists():
            return RecursiveCategorySerializer(
                obj.subcategories.all(), 
                many=True,
                context=self.context
            ).data
        return []