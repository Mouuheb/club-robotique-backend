from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserSerializer, UserUpgradeSerializer
from rest_framework.authtoken.models import Token

User = get_user_model()

@api_view(['POST'])
def register_user(request):
    """Allow anyone to create a member account"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        print('okk')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
# @permission_classes([IsAuthenticated, IsAdminUser])
def list_users(request):
    """Allow staff accounts to see all users"""
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def upgrade_user(request, user_id):
    """Allow superuser to upgrade member to staff or admin"""
    # Check if requester is superuser
    if not request.user.is_superuser:
        
        return Response(
            {"error": "Only superusers can perform upgrades"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {"error": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Prevent upgrading other superusers
    if user.is_superuser and user != request.user:
        return Response(
            {"error": "Cannot modify other superusers"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = UserUpgradeSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)