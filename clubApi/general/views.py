from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from .models import Activity, Sponsor
from .serializers import ActivitySerializer, SponsorSerializer

# Helper function to check superuser
def is_superuser(user):
    return user.is_superuser

# Activity Views
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def activity_list(request):
    """List activities or create new (superuser only)"""
    if request.method == 'GET':
        activities = Activity.objects.all()
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        
        # Only superuser can update/delete activity
        if not request.user.is_superuser:
            return Response(
                {"error": "Only superusers can modify activity"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = ActivitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def activity_detail(request, pk):
    """Retrieve, update or delete an activity (superuser only for write ops)"""
    try:
        activity = Activity.objects.get(pk=pk)
    except Activity.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ActivitySerializer(activity)
        return Response(serializer.data)

    # Write operations require superuser
    if not request.user.is_superuser:
        return Response(
            {"error": "Only superusers can modify activity"},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == 'PUT':
        serializer = ActivitySerializer(activity, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Sponsor Views (same pattern as Activity)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def sponsor_list(request):
    """List sponsors or create new (superuser only)"""
    if request.method == 'GET':
        sponsors = Sponsor.objects.all()
        serializer = SponsorSerializer(sponsors, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Only superuser can update/delete activity
        if not request.user.is_superuser:
            return Response(
                {"error": "Only superusers can modify activity"},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = SponsorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def sponsor_detail(request, pk):
    """Sponsor detail view"""
    try:
        sponsor = Sponsor.objects.get(pk=pk)
    except Sponsor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SponsorSerializer(sponsor)
        return Response(serializer.data)

    # Only superuser can update/delete activity
    if not request.user.is_superuser:
        return Response(
            {"error": "Only superusers can modify activity"},
            status=status.HTTP_403_FORBIDDEN
        )

    if request.method == 'PUT':
        serializer = SponsorSerializer(sponsor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        sponsor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)