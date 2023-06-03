from rest_framework import serializers
from rest_framework.exceptions import ParseError, NotAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User
from reviews.models import Review


class FollowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "pk",
            # "avatar",
            "nickname",
        )


class MyReviewSerializer(serializers.ModelSerializer):
    userPk = serializers.SerializerMethodField()
    likes = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    createdAt = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()

    def get_userPk(self, obj):
        return obj.user.pk

    def get_likes(self, obj):
        return obj.like_users.count()

    def get_comments(self, obj):
        return obj.comments.count()

    def get_createdAt(self, obj):
        return obj.created_at

    def get_code(self, obj):
        return obj.movie_code

    class Meta:
        model = Review
        fields = (
            "pk",
            "userPk",
            "code",
            "title",
            "content",
            "likes",
            "comments",
            "createdAt",
        )


class CreateUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True,
        required=True,
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )
    avatar = serializers.URLField(required=False)
    intro = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
            "nickname",
            "avatar",
            "intro",
        )

    def create(self, validated_data):
        password1 = validated_data.pop("password1", None)
        password2 = validated_data.pop("password2", None)

        if not password1 or not password2:
            return ParseError

        if password1 != password2:
            return ValueError

        user = super().create(validated_data)
        user.set_password(password1)
        user.save()

        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True,
        required=True,
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
    )
    avatar = serializers.URLField(required=False)
    intro = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            "password1",
            "password2",
            "nickname",
            "avatar",
            "intro",
        )

    def update(self, instance, validated_data):
        cur_password = validated_data.pop("password1", None)
        new_password = validated_data.pop("password2", None)

        user = super().update(instance, validated_data)

        if not cur_password or not new_password:
            return ParseError

        if not user.check_password(cur_password):
            raise ValueError

        user.set_password(new_password)
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    followings = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    def get_followings(self, obj):
        followings = obj.following
        serializer = FollowingSerializer(followings, many=True)
        return serializer.data

    def get_followers(self, obj):
        followers = obj.followers
        serializer = FollowingSerializer(followers, many=True)
        return serializer.data

    def get_reviews(self, obj):
        reviews = obj.reviews.order_by("-created_at")
        serializer = MyReviewSerializer(reviews, many=True)
        return serializer.data

    class Meta:
        model = User
        fields = [
            "pk",
            "avatar",
            "email",
            "nickname",
            "intro",
            "followings",
            "followers",
            "reviews",
        ]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["nickname"] = user.nickname
        return token
