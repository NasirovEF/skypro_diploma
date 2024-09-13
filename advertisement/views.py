from django.shortcuts import render
from rest_framework import viewsets

from advertisement.models import Ad, Feedback
from advertisement.serializers import AdSerializer, FeedbackSerializer


class AdViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с объявлениями"""

    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FeedbackViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с отзывами"""

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)