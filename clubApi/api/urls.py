from django.urls import path
from . import views

urlpatterns = [
    # Groups
    path('groups/', views.group_list, name='group-list'),
    
    path('groups/<int:pk>/', views.group_detail, name='group-detail'),
    path('groups/<int:pk>/add-member/', views.add_group_member, name='add-group-member'),
    path('groups/<int:pk>/join/', views.join_group, name='join-group'),
]