from rest_framework import serializers
from advertisement.models import Ad, Feedback
from advertisement.services.function import return_bad_words


class FeedbackSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с отзывами"""
    author = serializers.StringRelatedField(read_only=True)

    def validate(self, data):
        text = data.get('text')

        for word in return_bad_words():
            if word in text.lower():
                raise serializers.ValidationError("Нельзя использовать запретные слова")
        return data

    class Meta:
        model = Feedback
        fields = "__all__"


class AdUserAuntSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с объявлением для авторизованных пользователей"""
    feedback = FeedbackSerializer(many=True, read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    def validate(self, data):
        title = data.get('title')
        description = data.get('description')

        for word in return_bad_words():
            if word in title.lower() or word in description:
                raise serializers.ValidationError("Нельзя использовать запретные слова")
        return data

    class Meta:
        model = Ad
        fields = "__all__"


class AdSerializer(serializers.ModelSerializer):
    """Сериалайзер для работы с объявлением не авторизованных пользователей"""
    feedback_count = serializers.SerializerMethodField()

    def get_feedback_count(self, object):
        return object.feedback.count()

    class Meta:
        model = Ad
        fields = ("title", "description", "price", "feedback_count")
