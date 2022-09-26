from djoser.serializers import UserCreateSerializer as BaseUserRegistrationSerializer

from djoser.serializers import UserSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationSerializer(BaseUserRegistrationSerializer):

    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'phone',
            'role',
            'password',
        ]

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        user.set_password(validated_data["password"])

        user.save()
        return user


class CurrentUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'phone',
            'image',
        ]

    def save(self):
        user = super().save()
        user.save()
        return user
