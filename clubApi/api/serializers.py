from rest_framework import serializers
from .models import Group
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

User = get_user_model()

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'members']
        extra_kwargs = {
            'members': {'required': False}
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name']

class GroupMemberSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()