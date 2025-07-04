from rest_framework import permissions

def is_superuser(request):
    return request.user.is_superuser

def is_staff_member_of_group(request, group):
    return request.user.is_staff and group.members.filter(id=request.user.id).exists()