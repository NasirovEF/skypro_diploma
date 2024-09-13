from rest_framework import serializers

from advertisement.models import Ad, Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с отзывами"""
    author = serializers.StringRelatedField(read_only=True)
    ad = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Feedback
        fields = "__all__"


class AdSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с объявлением"""
    feedback = FeedbackSerializer(many=True)
    author = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Ad
        fields = "__all__"


