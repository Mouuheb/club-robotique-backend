from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

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

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError("User account is disabled.")
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")
        return data       
    
class UserUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, 
        required=False,
        allow_blank=True,
        style={'input_type': 'password'}
    )
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 
                 'description', 'label', 'xp', 'level', 'is_staff', 'is_superuser']
        extra_kwargs = {
            'email': {'required': False}
        }
    
    def update(self, instance, validated_data):
        # Handle password separately
        password = validated_data.pop('password', None)
        if password and password.strip() != "":
            instance.set_password(password)
        
        return super().update(instance, validated_data)