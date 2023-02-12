from rest_framework import serializers

from .models import Cart

from product.serializers import ProductsSerializer

class CartSerializer(serializers.ModelSerializer):
    products = ProductsSerializer(many=True)
    
    class Meta:
        model = Cart
        fields = ["id", "total",  "products"]
