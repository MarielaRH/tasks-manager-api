from rest_framework import serializers
from categories.models import Category

class CategoriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'created_at')