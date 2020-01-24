from rest_framework import status
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework.test import APITestCase
from .models import UserAccount, create_auth_token

# Create your tests here.


class RegistrationTestCase(APITestCase):
    """testing registration view"""

    def test_registration(self):
        data = {
            "email": "testuser12333@gmail.com",
            "username": "testuser12333",
            "name": "test",
            "password": "spongebob109",
            "confirm_password": "spongebob109",
        }

        response = self.client.post("/api/register", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_error(self):
        data = {
            "email": "testuser",
            "username": "dsadasd",
            "name": "",
            "password": "spongebob109",
            "confirm_passowrd": "spongebob"
        }
        response = self.client.post("/api/register", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetUserDataTestCase(APITestCase):
    """testing GET method for getting user data after authentication"""

    def setUp(self):
        self.user = UserAccount.objects.create_user(email="testuser109@gmail.com",
                                                    username="testuser109",
                                                    name="testuser",
                                                    password="spongebob109")
        self.token = create_auth_token(sender=self.user, instance=self.user)
        self.username = self.user.username
        # self.token = Token.objects.create(user=self.user)
        # self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.token = Token.objects.get(user_id=1)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + str(self.token.key))

    def test_get_user_data(self):
        response = self.client.get(reverse("anima_app:detail", kwargs={"username": self.username}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], "testuser109")

    def test_update_user_data(self):
        data = {
            "name": "giorgi45"
        }
        response = self.client.patch(reverse("anima_app:partial_update", kwargs={"username": self.username}), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "giorgi45")

    def test_update_user_data_error(self):
        data = {
            "username": ""
        }
        response = self.client.patch(reverse("anima_app:partial_update", kwargs={"username": self.username}), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password(self):
        data = {
            "old_password": "spongebob109",
            "new_password": "spongebob1099"
        }
        response = self.client.post(reverse("anima_app:password_change"), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password_error(self):
        data = {
            "old_password": "spongebob12",
            "new_password": "spongebob1099"
        }
        response = self.client.post(reverse("anima_app:password_change"), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_user(self):
        data = {
            "password": "spongebob109"
        }
        response = self.client.delete(reverse("anima_app:delete_user", kwargs={"username": self.username}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user_error(self):
        data = {
            "password": "spongebob12"
        }
        response = self.client.delete(reverse("anima_app:delete_user", kwargs={"username": self.username}), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



