
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
    def create_product(name="", price=0.00):
        return Products.objects.create(name=name, price=price)

    def login_client(self, username="", password=""):
        response = self.client.post(
            reverse("create-token"),
            data=json.dumps(
                {
                    "username": username,
                    "password": password
                }
            ),
            content_type="application/json"
        )

        self.token = response.data["token"]
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.token
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

        self.product_001 = self.create_product("Rice", 4.50)
        self.create_product("Milk", 2.20)
        self.create_product("Eggs", 1.00)

class getAllProductsTest(BaseViewTest):
    def test_create_product(self):
        self.login_client("test_user", "testing")

        response = self.client.post(reverse("products"), {
            "name": "product_test",
            "price": 0
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_get_product(self):
        self.login_client("test_user", "testing")
        expected = Products.objects.get(pk=self.product_001.id)
        serialized = ProductsSerializer(expected)

        response = self.client.get(reverse("product-details", kwargs={
            "pk": self.product_001.id
        }))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized.data)

    def test_get_all_products(self):
        expected = Products.objects.all()
        serialized = ProductsSerializer(expected, many=True)
        
        self.login_client("test_user", "testing")
        
        response = self.client.get(reverse("products"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized.data)
    
    def test_update_product(self):
        self.login_client("test_user", "testing")

        response = self.client.put(reverse("product-details", kwargs={
            "pk": self.product_001.id
        }), {
            "name": "product_updated",
            "price": 10.0,
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        expected = Products.objects.get(pk=self.product_001.id)
        serialized = ProductsSerializer(expected)
        self.assertEqual(response.data, serialized.data)

    def test_delete_product(self):
        self.login_client("test_user", "testing")

        response = self.client.delete(reverse("product-details", kwargs={
            "pk": self.product_001.id
        }))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        