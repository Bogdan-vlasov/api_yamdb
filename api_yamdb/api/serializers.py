from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from users.models import User


class SerializerUsers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class SerializerNotAdmin(serializers.ModelSerializer):
    role = serializers.CharField(
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class SerializerToken(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class SerializerSignUp(serializers.ModelSerializer):
    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError('Запрещенный логин me')
        return data

    def create(self, validated_data):
        return User.objects.create(**validated_data)

    class Meta:
        model = User
        fields = ('username', 'email')
        validators = [UniqueTogetherValidator(
            queryset=User.objects.all(), fields=['username', 'email'],
            message='Username или email уже используются'
        )]
