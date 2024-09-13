from django.db import models

from users.models import User
from users.services import NULLABLE


class Ad(models.Model):
    """Модель объявления"""

    title = models.CharField(max_length=100, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание товара")
    price = models.PositiveIntegerField(verbose_name="Цена товара")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь создавший объявление",
        related_name="ad",
        **NULLABLE
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время создания объявления"
    )

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Feedback(models.Model):
    """Модель отзыва"""
    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор отзыва", related_name="feedback", **NULLABLE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, verbose_name="Объявление", related_name="feedback", **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время создания отзыва")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]
