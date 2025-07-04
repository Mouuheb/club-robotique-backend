from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UserSerializer, UserUpgradeSerializer
from rest_framework.authtoken.models import Token
from .serializers import UserLoginSerializer


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
@permission_classes([IsAuthenticated, IsAdminUser])
def list_users(request):
    """Allow staff accounts to see all users"""
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    """Log out the current user by deleting their token"""
    try:
        # Delete the user's token to logout
        request.user.auth_token.delete()
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_user(request, user_id):
    """Allow superuser to delete a user"""
    # Check if requester is superuser
    if not request.user.is_superuser:
        return Response(
            {"error": "Only superusers can delete users"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        user_to_delete = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {"error": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Prevent deleting yourself
    if user_to_delete == request.user:
        return Response(
            {"error": "You cannot delete yourself"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    # Prevent deleting other superusers
    if user_to_delete.is_superuser:
        return Response(
            {"error": "Cannot delete other superusers"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    user_to_delete.delete()
    return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def custom_login(request):
    """Custom login view that returns user data along with token"""
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        # Return user data along with token
        return Response({
            'token': token.key,
            'user_id': user.id,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)