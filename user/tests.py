
import json
from django.contrib.auth.models import User

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status

class BaseViewTest(APITestCase):
    client = APIClient()
    
    def login_a_user(self, username="", password=""):
        url = reverse(
            "auth-login"
        )

        return self.client.post(
            url,
            data=json.dumps({
                "username": username,
                "password": password
            }),
            content_type="application/json"
        )

    def register_a_user(self, username="", password="", email=""):
        return self.client.post(
            reverse(
                "auth-register"
            ),
            data=json.dumps(
                {
                    "username": username,
                    "password": password,
                    "email": email
                }
            ),
            content_type='application/json'
        )

    
    def setUp(self):
        self.user = User.objects.create_superuser(
            username="test_user",
            email="test@mail.com",
            password="testing",
            first_name="test",
            last_name="user",
        )

class AuthLoginUserTest(BaseViewTest):
    def test_login_user_with_valid_credentials(self):
        response = self.login_a_user("test_user", "testing")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        
        response = self.login_a_user("anonymous", "pass")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthRegisterUserTest(BaseViewTest):
    def test_register_a_user(self):
        response = self.register_a_user("new_user", "new_pass", "new_user@mail.com")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "new_user")
        self.assertEqual(response.data["email"], "new_user@mail.com")
        
        response = self.register_a_user()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)