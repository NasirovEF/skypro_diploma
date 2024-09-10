import secrets
from rest_framework.views import Response, status
from django.core.mail import send_mail
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from django.http import Http404
from config.settings import EMAIL_HOST_USER
from users.models import User
from users.serializers import UserResetPassword, UserSerializer


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


@api_view("GET")
def user_reset_password(request):
    try:
        user = User.objects.get(email=request.data.get("email"))
    except User.DoesNotExist:
        raise Http404

    if request.method == "GET":
        serializer = UserResetPassword(user)
        user = serializer.save()
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = request.get_host()
        url = f"https//{host}/users/reset-password_confirm/{user.pk}/{user.token}"
        send_mail(
            subject=f"Сброс пароля для {User.objects.get(email=user.email)}",
            message=f"Для сброса пароля отправьте POST запрос по ссылке {url}, указав новый пароль: new_password: ******",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return (
            f"Данные для сброса направлены Вам на почту {request.data.get('email')}"
        )


@api_view("POST")
def user_reset_password_confirm(request, pk, token):
    try:
        user = User.objects.get(pk=pk, token=token)
    except User.DoesNotExist:
        raise Http404
    if request.method == "POST":
        new_password = request.data.get("password")
        user.set_password(new_password)
        user.save()
        return "Пароль успешно изменен"
