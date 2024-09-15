
from rest_framework import viewsets

from advertisement.paginations import AdListViewPagination
from advertisement.permissions import IsOwnerPermission
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from advertisement.models import Ad, Feedback
from advertisement.serializers import AdSerializer, FeedbackSerializer, AdUserAuntSerializer


class AdViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с объявлениями"""

    queryset = Ad.objects.all()
    pagination_class = AdListViewPagination

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
           self.serializer_class = AdUserAuntSerializer
        else:
           self.serializer_class = AdSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ('create', 'retrieve'):
            self.permission_classes = (IsAuthenticated,)
        elif self.action == 'list':
            self.permission_classes = (AllowAny,)
        elif self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes = (IsOwnerPermission | IsAdminUser,)
        return super().get_permissions()


class FeedbackViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с отзывами"""

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in ('create', 'retrieve', 'list'):
            self.permission_classes = (IsAuthenticated,)
        elif self.action in ('update', 'partial_update', 'destroy'):
            self.permission_classes = (IsOwnerPermission | IsAdminUser,)
        return super().get_permissions()
