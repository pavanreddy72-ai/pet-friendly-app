
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

TEST_PASSWORD = "Strong-Test-Password-123!"


class UserModelTests(TestCase):
    def test_create_user_normalizes_email(self):
        user = User.objects.create_user(
            email="TestUser@Example.com",
            password=TEST_PASSWORD,
        )

        self.assertEqual(user.email, "testuser@example.com")
        self.assertTrue(user.check_password(TEST_PASSWORD))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser_sets_admin_permissions(self):
        admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password=TEST_PASSWORD,
        )

        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

    def test_email_is_unique(self):
        User.objects.create_user(
            email="duplicate@example.com",
            password=TEST_PASSWORD,
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                User.objects.create_user(
                    email="duplicate@example.com",
                    password="Another-Strong-Password-456!",
                )


class RegistrationAPITests(APITestCase):
    register_url = "/api/auth/register/"

    def test_register_user_successfully(self):
        payload = {
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "password": TEST_PASSWORD,
        }

        response = self.client.post(self.register_url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["email"], "newuser@example.com")
        self.assertNotIn("password", response.data)

        user = User.objects.get(email="newuser@example.com")
        self.assertTrue(user.check_password(TEST_PASSWORD))

    def test_duplicate_email_is_rejected(self):
        User.objects.create_user(
            email="existing@example.com",
            password=TEST_PASSWORD,
        )

        response = self.client.post(
            self.register_url,
            {
                "email": "existing@example.com",
                "password": TEST_PASSWORD,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_weak_password_is_rejected(self):
        response = self.client.post(
            self.register_url,
            {
                "email": "weakpass@example.com",
                "password": "123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(
            User.objects.filter(email="weakpass@example.com").exists()
        )


class LoginAPITests(APITestCase):
    login_url = "/api/auth/login/"
    refresh_url = "/api/auth/token/refresh/"

    def setUp(self):
        self.user = User.objects.create_user(
            email="login@example.com",
            password=TEST_PASSWORD,
        )

    def test_login_returns_jwt_tokens(self):
        response = self.client.post(
            self.login_url,
            {"email": "login@example.com", "password": TEST_PASSWORD},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_wrong_password_is_rejected(self):
        response = self.client.post(
            self.login_url,
            {"email": "login@example.com", "password": "Wrong-Password-123!"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_returns_new_access_token(self):
        login_response = self.client.post(
            self.login_url,
            {"email": "login@example.com", "password": TEST_PASSWORD},
            format="json",
        )

        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            self.refresh_url,
            {"refresh": login_response.data["refresh"]},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
