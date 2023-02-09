from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_jwt_token, name='create-token'),
    path('api-token-refresh/', refresh_jwt_token),
    path('users/', include('user.urls')),
    path('products/', include('product.urls'))
]
