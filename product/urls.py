from django.urls import path
from .views import ListProductsView


urlpatterns = [
    path('', ListProductsView.as_view(), name="products-all"),
]