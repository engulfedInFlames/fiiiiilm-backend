from rest_framework import serializers
from reviews.models import Review, Comment


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)


class CommentListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.email

    class Meta:
        model = Comment
        fields = "__all__"


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "title",
            "content",
            "movie_code",
        )


class ReviewListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()
    like_user_pk = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname

    def get_avatar(self, obj):
        return obj.user.avatar

    def get_comment_count(self, obj):
        return Comment.objects.filter(review=obj).count()

    def get_like_count(self, obj):
        return obj.like_users.count()

    def get_like_user_pk(self, obj):
        queryset = obj.like_users.values("pk")

        return [item["pk"] for item in queryset]

    class Meta:
        model = Review
        exclude = ("like_users",)


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comments = CommentListSerializer(many=True)
    comment_count = serializers.SerializerMethodField()
    like_count = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.nickname

    def get_comment_count(self, obj):
        return Comment.objects.filter(review=obj).count()

    def get_like_count(self, obj):
        return obj.like_users.count()

    class Meta:
        model = Review
        fields = "__all__"
