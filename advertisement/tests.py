from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls  import reverse

from advertisement.models import Ad, Feedback
from users.models import User
from rest_framework import status


class AdTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test05@test.ru")
        self.ad = Ad.objects.create(title="Skypro", description="курс скайпро", price=100000)
        self.client.force_authenticate(user=self.user)
        print(Ad.objects.all())

    def test_ad_retrieve(self):

        url = reverse("advertisement:ad", args=(self.ad.pk,))
        response = self.client.get(url)
        print(response)
        data = response.json()
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.ad.title)

