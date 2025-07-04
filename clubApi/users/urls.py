from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('users/', views.list_users, name='user-list'),
    path('users/<int:user_id>/upgrade/', views.upgrade_user, name='user-upgrade'),

    path('login/', views.custom_login, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('users/<int:user_id>/delete/', views.delete_user, name='user-delete'),

    path('users/<int:pk>/', views.user_detail, name='user-detail'),
]