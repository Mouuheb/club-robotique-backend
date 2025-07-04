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
from .models import Task, Event
from .serializers import TaskSerializer, EventSerializer


User = get_user_model()

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

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def task_detail(request, task_id):
    """Retrieve, update or delete a task"""
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response(
            {"error": "Task not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = TaskSerializer(task)
        return Response(serializer.data)
    
    # Only superuser can update/delete tasks
    if not request.user.is_superuser:
        return Response(
            {"error": "Only superusers can modify tasks"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    if request.method == 'PUT':
        # serializer = TaskSerializer(data=request.data, )
        serializer = TaskSerializer(task, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def assign_task(request, task_id):
    """Assign a task to the current user"""
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return Response(
            {"error": "Task not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Assign task to current user
    task.user = request.user
    task.save()
    return Response(
        {"message": "Task assigned to you successfully"},
        status=status.HTTP_200_OK
    )

# Event Views

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def event_detail(request, event_id):
    """Retrieve, update or delete an event"""
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response(
            {"error": "Event not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    # Only superuser can update/delete events
    if not request.user.is_superuser:
        return Response(
            {"error": "Only superusers can modify events"},
            status=status.HTTP_403_FORBIDDEN
        )
    
    if request.method == 'PUT':
        serializer = EventSerializer(event, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_event(request, event_id):
    """Add current user to event attendees"""
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response(
            {"error": "Event not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Add user to event attendees
    if not event.users.filter(id=request.user.id).exists():
        event.users.add(request.user)
        return Response(
            {"message": "You have joined the event"},
            status=status.HTTP_200_OK
        )
    return Response(
        {"message": "You are already attending this event"},
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def leave_event(request, event_id):
    """Remove current user from event attendees"""
    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response(
            {"error": "Event not found"},
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Remove user from event attendees
    if event.users.filter(id=request.user.id).exists():
        event.users.remove(request.user)
        return Response(
            {"message": "You have left the event"},
            status=status.HTTP_200_OK
        )
    return Response(
        {"message": "You were not attending this event"},
        status=status.HTTP_200_OK
    )



# Task Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def task_list(request):
    """List tasks or create new task (staff/superuser)"""
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Only staff/superuser can create tasks
        if not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {"error": "Only staff or superusers can create tasks"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Handle category ID
        data = request.data.copy()
        category_id = data.get('category_id')
        
        # Validate category if provided
        if category_id:
            try:
                category = Group.objects.get(id=category_id)
            except Group.DoesNotExist:
                return Response(
                    {"error": "Group not found"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # serializer = TaskSerializer(data=data)
        serializer = TaskSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            task = serializer.save(created_by=request.user)
            
            # Set category if provided
            if category_id:
                task.category = category
                task.save()
            
            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Event Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def event_list(request):
    """List events or create new event (superuser only)"""
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Only superuser can create events
        if not request.user.is_superuser:
            return Response(
                {"error": "Only superusers can create events"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = EventSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Create event and add creator to attendees
            event = serializer.save(created_by=request.user)
            event.users.add(request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
