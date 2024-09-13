from django.urls import include, path
from rest_framework.routers import DefaultRouter

from advertisement import views
from advertisement.apps import AdvertisementConfig

app_name = AdvertisementConfig.name

router = DefaultRouter()
router.register(r"ads", views.AdViewSet, basename="ad")
router.register(r"feedbacks", views.FeedbackViewSet, basename="feedback")

urlpatterns = [path("", include(router.urls))]
