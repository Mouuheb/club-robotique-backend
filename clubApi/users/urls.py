from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('users/', views.list_users, name='user-list'),
    path('users/<int:user_id>/upgrade/', views.upgrade_user, name='user-upgrade'),
]