
import json
from django.contrib.auth.models import User

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Products
from .serializers import ProductsSerializer

class BaseViewTest(APITestCase):
    client = APIClient()

    @staticmethod
    def create_product(name='', price=0.00):
        Products.objects.create(name=name, price=price)

    def login_client(self, username="", password=""):
        response = self.client.post(
            reverse("create-token"),
            data=json.dumps(
                {
                    'username': username,
                    'password': password
                }
            ),
            content_type='application/json'
        )

        self.token = response.data['token']
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + self.token
        )
        self.client.login(username=username, password=password)
        
        return self.token

    
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="test_user",
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user",
        )

        self.create_product('Rice', 4.50)
        self.create_product('Milk', 2.20)
        self.create_product('Eggs', 1.00)

class getAllProductsTest(BaseViewTest):
    def test_get_all_products(self):
        expected = Products.objects.all()
        serialized = ProductsSerializer(expected, many=True)
        
        self.login_client('test_user', 'testing')
        
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized.data)