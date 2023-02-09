from rest_framework import permissions
from rest_framework import generics

from .models import Products
from .serializers import ProductsSerializer

class ListProductsView(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    permission_classes = (permissions.IsAuthenticated,)
