
from rest_framework.test import APITestCase
from django.urls import reverse

from users.models import User
from rest_framework import status

class UserTestCase(APITestCase):
    def test_user_create(self):
        """Создание нового пользователя"""
        url = reverse('users:create')
        data = {
            'email': 'test05@test.ru',
            'password': 'test123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test05@test.ru')
