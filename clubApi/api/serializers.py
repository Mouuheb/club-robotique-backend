from rest_framework import serializers
from .models import Task, Event, Group
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



class TaskSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(
        read_only=True, 
        default=serializers.CurrentUserDefault()
    )
    category = GroupSerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'deadline', 'xp', 'description', 
            'user', 'category', 'category_id', 'created_by', 'created_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'xp', 'category']
    
    def validate_category_id(self, value):
        if value is not None:
            try:
                Group.objects.get(id=value)
            except Group.DoesNotExist:
                raise serializers.ValidationError("Group not found")
        return value


class EventSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(
        read_only=True, 
        default=serializers.CurrentUserDefault()
    )
    users = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False
    )
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'date', 'location', 'description', 'image_link',
            'users', 'created_by', 'created_at'
        ]
        read_only_fields = ['created_by', 'created_at']

        