from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'description', 'label', 'xp', 'level', 'token']
        extra_kwargs = {
            'xp': {'read_only': True},
            'level': {'read_only': True},
        }

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key

    def create(self, validated_data):
        # Create user with member permissions
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            description=validated_data.get('description', ''),
            label=validated_data.get('label', ''),
            is_staff=False,
            is_superuser=False
        )
        # Token.objects.create(user=user)  # Create token but don't return it
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'description', 'label', 'xp', 'level', 'is_staff', 'is_superuser']
        read_only_fields = ['is_staff', 'is_superuser', 'xp', 'level']

class UserUpgradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_staff', 'is_superuser']