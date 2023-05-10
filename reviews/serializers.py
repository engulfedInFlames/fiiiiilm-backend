from rest_framework import serializers
from reviews.models import Review, Comment


class CommentListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.email

    class Meta:
        model = Comment
        fields = "__all__"


class ReviewListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comments = CommentListSerializer(many=True)

    def get_user(self, obj):
        return obj.user.nickname

    class Meta:
        model = Review
        fields = "__all__"


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("title", "content", "movie_code",)


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)
