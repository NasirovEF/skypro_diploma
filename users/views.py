import secrets

from django.core.mail import send_mail
from django.http import Http404
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from config.settings import EMAIL_HOST_USER
from users.models import User
from users.serializers import UserResetPassword, UserSerializer


class UserCreate(generics.CreateAPIView):
    """Вьюшка создания пользователя"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


@api_view(
    [
        "PUT",
    ]
)
@permission_classes([AllowAny])
def user_reset_password(request):
    """Вьюшка для инициализации сброса пароля"""
    try:
        user = User.objects.get(email=request.data.get("email"))
    except User.DoesNotExist:
        raise Http404

    if request.method == "PUT":
        serializer = UserResetPassword(user, data=request.data)
        if serializer.is_valid():
            token = secrets.token_hex(16)
            user.token_for_password = token
            user.save()
            host = request.get_host()
            url = f"https://{host}/users/reset_password_confirm/{user.pk}/{user.token_for_password}/"
            send_mail(
                subject=f"Сброс пароля для {User.objects.get(email=user.email)}",
                message=f"Для сброса пароля отправьте PUT запрос по ссылке {url}, указав новый пароль: new_password: ******",
                from_email=EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
            return Response(
                f"Данные для сброса направлены Вам на почту {request.data.get('email')}"
            )


@api_view(
    [
        "PUT",
    ]
)
@permission_classes([AllowAny])
def user_reset_password_confirm(request, pk, token_for_password):
    """Вьюшка для подтверждения сброса пароля"""
    try:
        user = User.objects.get(pk=pk, token_for_password=token_for_password)
    except User.DoesNotExist:
        raise Http404
    if request.method == "PUT":
        new_password = request.data.get("new_password")
        user.set_password(new_password)
        user.save()
        return Response("Пароль успешно изменен")
