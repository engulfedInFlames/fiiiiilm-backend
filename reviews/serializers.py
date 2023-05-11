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
    comments = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname

    def get_comments(self, obj):
        return Comment.objects.filter(review=obj).count()

    def get_like_count(self, obj):
        return obj.like_users.count()

    class Meta:
        model = Review
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname

    def get_comments(self, obj):
        return Comment.objects.filter(review=obj).count()

    def get_like_count(self, obj):
        return obj.like_users.count()

    class Meta:
        model = Review
        fields = "__all__"
        # exclude = ('like_users',)


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ("title", "content", "movie_code",)


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)
