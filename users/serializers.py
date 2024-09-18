from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с пользователем"""

    class Meta:
        model = User
        fields = "__all__"


class UserResetPassword(serializers.ModelSerializer):
    """Сериалайзер для сброса пароля"""

    class Meta:
        model = User
        fields = ("email",)
