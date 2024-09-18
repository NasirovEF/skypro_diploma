
from rest_framework.test import APITestCase
from django.urls import reverse

from advertisement.models import Ad, Feedback
from users.models import User
from rest_framework import status


class AdTestCase(APITestCase):

    def setUp(self):
        """Установка начальных параметров"""
        self.user = User.objects.create(email="test05@test.ru")
        self.ad = Ad.objects.create(title="Skypro", description="курс скайпро", price=100000, author=self.user)
        self.client.force_authenticate(user=self.user)

    def test_ad_retrieve(self):
        """Просмотр одного объявления"""
        url = reverse("advertisement:ad-detail", args=(self.ad.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.ad.title)

    def test_ad_delete(self):
        """Удаление объявления"""
        url = reverse("advertisement:ad-detail", args=(self.ad.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ad.objects.count(), 0)

    def test_ad_update(self):
        """Изменение объявления"""
        url = reverse("advertisement:ad-detail", args=(self.ad.pk,))
        data = {"title": "Skypro updated", "description": "курс скайпро updated", "price": 110000}
        response = self.client.put(url, data=data)
        url_new = reverse("advertisement:ad-detail", args=(self.ad.pk,))
        response_new = self.client.get(url_new)
        data_new = response_new.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_new.get("title"), "Skypro updated")

    def test_ad_create(self):
        """Создание нового объявления"""
        url = reverse("advertisement:ad-list")
        data = {"title": "Skypro new", "description": "курс скайпро new", "price": 120000}
        response = self.client.post(url, data=data)
        url_new = reverse("advertisement:ad-detail", kwargs={"pk": 2})
        response_new = self.client.get(url_new)
        data_new = response_new.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data_new.get("author"), self.user.email)
        self.assertEqual(Ad.objects.count(), 2)

    def test_ad_perm_retrieve(self):
        """Тест прав доступа на просмотр одного объявления анонимным пользователем"""
        self.client.logout()
        url = reverse("advertisement:ad-detail", args=(self.ad.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ad_anon_delete(self):
        """Тест прав доступа на удаление объявления анонимным пользователем"""
        self.client.force_authenticate(user=None)
        url = reverse("advertisement:ad-detail", args=(self.ad.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ad_perm_delete(self):
        """Тест прав доступа на удаление объявления пользователем, не являющимся автором или админом"""
        self.user = User.objects.create(email="user@example.com")
        self.client.force_authenticate(user=self.user)
        url = reverse("advertisement:ad-detail", args=(self.ad.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class FeedbackTestCase(APITestCase):

    def setUp(self):
        """Установка начальных параметров"""
        self.user = User.objects.create(email="test05@test.ru")
        self.ad = Ad.objects.create(title="Skypro", description="курс скайпро", price=100000, author=self.user)
        self.feedback = Feedback.objects.create(ad=self.ad, text="Отличный курс!", author=self.user)
        self.client.force_authenticate(user=self.user)

    def test_feedback_retrieve(self):
        """Просмотр одного отзыва"""
        url = reverse("advertisement:feedback-detail", args=(self.feedback.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("text"), self.feedback.text)

    def test_feedback_delete(self):
        """Удаление отзыва"""
        url = reverse("advertisement:feedback-detail", args=(self.feedback.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Feedback.objects.count(), 0)

    def test_feedback_update(self):
        """Изменение отзыва"""
        url = reverse("advertisement:feedback-detail", args=(self.feedback.pk,))
        data = {"text": "Text updated", "ad": self.ad.pk}
        response = self.client.put(url, data=data)
        url_new = reverse("advertisement:feedback-detail", args=(self.feedback.pk,))
        response_new = self.client.get(url_new)
        data_new = response_new.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data_new.get("text"), "Text updated")

    def test_feedback_create(self):
        """Создание нового отзыва"""
        url = reverse("advertisement:feedback-list")
        data = {"text": "Skypro new comm", "ad": self.ad.pk}
        response = self.client.post(url, data=data)
        url_new = reverse("advertisement:feedback-detail", kwargs={"pk": 2})
        response_new = self.client.get(url_new)
        data_new = response_new.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data_new.get("author"), self.user.email)
        self.assertEqual(Feedback.objects.count(), 2)

    def test_feedback_perm_retrieve(self):
        """Тест прав доступа на просмотр одного отзыва анонимным пользователем"""
        self.client.logout()
        url = reverse("advertisement:feedback-detail", args=(self.feedback.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_feedback_perm_delete(self):
        """Тест прав доступа на удаление отзыва пользователем, не являющимся автором или админом"""
        self.user = User.objects.create(email="user@example.com")
        self.client.force_authenticate(user=self.user)
        url = reverse("advertisement:feedback-detail", args=(self.feedback.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

