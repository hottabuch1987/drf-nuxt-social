from rest_framework import serializers
from .models import Category, Product



class ProductSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    owner_username = serializers.CharField(source='category.owner.username', read_only=True)
    class Meta:
        model = Product
        fields = [
                "owner_username",
                "category",
                "id",
                'name',
                "get_absolute_url",
                "date_added",
                "description",
                "get_image",
                "image",
                "slug",
                "get_video",
                "video",
                'likes_count', 
                "is_published",            
        ]
        
class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, required=False)
    owner_username = serializers.CharField(source='owner.username', read_only=True)



    class Meta:
        model = Category
        fields = [
                "id",
                "name",
                "slug",
                "products",
                "get_absolute_url",
                "owner",
                "owner_username",
                "date_added"       
                
        ]

    def create(self, validated_data):
        products_data = validated_data.pop('products', [])
        category = Category.objects.create(**validated_data)
        for product_data in products_data:
            Product.objects.create(category=category, **product_data)
        return category


