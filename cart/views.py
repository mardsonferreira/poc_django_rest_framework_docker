from django.http import Http404

from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from product.models import Products
from .models import Cart

from .serializers import CartSerializer

class CartList(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = Cart.objects.all()
        serializer = CartSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        total = data.get("total", None)
        products = data.get("products", None)

        if not total:
            return Response({"error": "MISSING_TOTAL_FIELD"}, status=status.HTTP_400_BAD_REQUEST)

        if not products:
            return Response({"error": "MISSING_PRODUCTS_FIELD"}, status=status.HTTP_400_BAD_REQUEST)
        
        products_queryset = Products.objects.filter(id__in=products)

        if not products_queryset:
            return Response({"error": "PRODUCTS_NOT_FOUND"}, status=status.HTTP_404_NOT_FOUND)
        
        cart = Cart.objects.create(total=total)

        for product in products_queryset:
            cart.products.add(product)

        return Response({"id": cart.id}, status=status.HTTP_201_CREATED)

class CartDetail(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self, pk):
        try:
            return Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        cart = self.get_object(pk)
        serializer = CartSerializer(cart)

        return Response(serializer.data)

        