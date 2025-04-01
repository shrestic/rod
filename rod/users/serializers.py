from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from djoser.serializers import UserSerializer as BaseUserSerializer
from rest_framework import serializers

from rod.core.exceptions import ApplicationError


class UserCreateSerializer(BaseUserCreateSerializer):
    re_password = serializers.CharField(write_only=True, required=True)

    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
            "re_password",
        ]

    def validate(self, attrs):
        password = attrs.get("password")
        re_password = attrs.get("re_password")

        if password and re_password and password != re_password:
            raise ApplicationError(message="Passwords do not match.")

        return attrs

    def create(self, validated_data):
        validated_data.pop("re_password", None)
        first_name = validated_data.pop("first_name", "")
        last_name = validated_data.pop("last_name", "")
        user = super().create(validated_data)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return user


class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ["id", "username", "email", "first_name", "last_name"]
