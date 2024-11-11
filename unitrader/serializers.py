# serializers.py
from rest_framework import serializers
from .models import Product, Category, Review, Landing, Navigation

class ProductCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    price = serializers.FloatField()
    count = serializers.IntegerField()
    color = serializers.CharField(max_length=50)
    image = serializers.URLField()
    categories = serializers.ListField(child=serializers.CharField(max_length=50))


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['slug', 'title', 'description', 'image', 'price', 'count', 'color', 'category']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['slug', 'title', 'description', 'image']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['slug', 'product', 'title', 'rating', 'content']

class LandingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Landing
        fields = ['slug', 'title', 'description', 'hero_image']

class NavigationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Navigation
        fields = ['slug', 'title', 'link', 'order']
