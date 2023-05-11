from dataclasses import field
from rest_framework import serializers
from rest_framework.exceptions import ParseError, NotAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # model = User
        # fields = ["email", "password", "nickname", "intro",]
        # extra_kwargs = {
        #     "password": {
        #         "write_only": True
        #     },
        # }

        model = User
        fields = [
            "email",
            "nickname",
            "intro",
        ]

    # def create(self, validated_data):
    #     user = super().create(validated_data)
    #     password = validated_data.get('password')
    #     user.set_password(password)
    #     user.nickname = f"user#{user.id}"
    #     user.save()
    #     return user

    def update(self, instance, validated_data):
        # password = user.password

        cur_password = validated_data.pop("password1", None)
        new_password = validated_data.pop("password2", None)

        if all(cur_password, new_password):
            return ParseError

        if not user.check_password(cur_password):
            raise NotAuthenticated

        user = super().update(instance, validated_data)
        user.set_password(new_password)
        user.save()

        return user


class FollowSerializer(serializers.ModelSerializer):
    followers = serializers.StringRelatedField(many=True)
    following = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ["following", "followers"]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["nickname"] = user.nickname
        return token
