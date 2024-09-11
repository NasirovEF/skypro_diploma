from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import UserCreate, user_reset_password, user_reset_password_confirm

app_name = UsersConfig.name

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("create/", UserCreate.as_view(), name="create"),
    path("reset_password/", user_reset_password, name="reset_password"),
    path("reset_password_confirm/<int:pk>/<str:token_for_password>/", user_reset_password_confirm, name="reset_password")
]
