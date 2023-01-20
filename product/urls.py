from django.urls import path
from .views import ListProductsView, LoginView, RegisterUsers


urlpatterns = [
    path('products/', ListProductsView.as_view(), name="products-all"),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('auth/register/', RegisterUsers.as_view(), name="auth-register")
]