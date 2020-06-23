from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import reverse
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APITestCase


class AuthTestCase(APITestCase):
    def test_login(self):
        url = reverse('login')
        data = {
            'username': 'admin',
            'password': 'admin'
        }

        User.objects.create_superuser('admin', '', 'admin')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertContains(response, 'token')

    def test_user_info(self):
        url = reverse('user_info-list')

        admin = User.objects.create_superuser('admin', '', 'admin')
        token = Token.objects.create(user=admin)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data['id'], admin.id)
        self.assertEqual(response.data['username'], admin.username)

    def test_logout(self):
        url = reverse('logout')

        admin = User.objects.create_superuser('admin', '', 'admin')
        token = Token.objects.create(user=admin)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTP_200_OK)
