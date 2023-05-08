from rest_framework import serializers
from reviews.models import Review


class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        # exclude = ("like_users",)


class CreateReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("title", "content",)
