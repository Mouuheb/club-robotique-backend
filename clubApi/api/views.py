from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Group
from .serializers import GroupSerializer, UserSerializer, GroupMemberSerializer
from .permissions import is_superuser, is_staff_member_of_group
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

User = get_user_model()
# Group Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def group_list(request):
    """List groups or create new group"""
    if request.method == 'GET':
        # Filter groups based on user permissions
        if is_superuser(request):
            groups = Group.objects.all()
        elif request.user.is_staff:
            groups = Group.objects.filter(members=request.user)
        else:
            groups = Group.objects.none()
        
        serializer = GroupSerializer(groups, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Only superusers can create groups
        if not is_superuser(request):
            return Response(
                {'error': 'Only superusers can create groups'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            group = serializer.save()
            # Add creator to the group
            group.members.add(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def group_detail(request, pk):
    """Retrieve, update or delete a group"""
    try:
        group = Group.objects.get(pk=pk)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Check permissions
    if not is_superuser(request) and not is_staff_member_of_group(request, group):
        return Response(
            {'error': 'You do not have permission for this group'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    if request.method == 'GET':
        serializer = GroupSerializer(group)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        # Only superusers can modify groups
        if not is_superuser(request):
            return Response(
                {'error': 'Only superusers can modify groups'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        # Only superusers can delete groups
        if not is_superuser(request):
            return Response(
                {'error': 'Only superusers can delete groups'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_group_member(request, pk):
    """Add a user to a group"""
    try:
        group = Group.objects.get(pk=pk)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Check permissions
    if not is_superuser(request) and not is_staff_member_of_group(request, group):
        return Response(
            {'error': 'You do not have permission for this group'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    serializer = GroupMemberSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user_id = serializer.validated_data['user_id']
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {'error': 'User not found'},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Add user to group
    group.members.add(user)
    return Response(
        {'status': f'User {user.email} added to group'},
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_group(request, pk):
    """Superuser joins a group"""
    if not is_superuser(request):
        return Response(
            {'error': 'Only superusers can join groups'},
            status=status.HTTP_403_FORBIDDEN
        )
    
    try:
        group = Group.objects.get(pk=pk)
    except Group.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    # Check if already in group
    if group.members.filter(id=request.user.id).exists():
        return Response(
            {'status': 'User already in group'},
            status=status.HTTP_200_OK
        )
    
    # Add user to group
    group.members.add(request.user)
    return Response(
        {'status': f'User joined group {group.name}'},
        status=status.HTTP_200_OK
    )
