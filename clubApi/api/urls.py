from django.urls import path
from . import views

urlpatterns = [
    # Groups
    path('groups/', views.group_list, name='group-list'),
    path('groups/<int:pk>/', views.group_detail, name='group-detail'),
    path('groups/<int:pk>/add-member/', views.add_group_member, name='add-group-member'),
    path('groups/<int:pk>/join/', views.join_group, name='join-group'),
    
    path('tasks/', views.task_list, name='task-list'),
    path('tasks/<int:task_id>/', views.task_detail, name='task-detail'),
    path('tasks/<int:task_id>/assign/', views.assign_task, name='assign-task'),
    
    # Event endpoints
    path('events/', views.event_list, name='event-list'),
    path('events/<int:event_id>/', views.event_detail, name='event-detail'),
    path('events/<int:event_id>/join/', views.join_event, name='join-event'),
    path('events/<int:event_id>/leave/', views.leave_event, name='leave-event'),


]