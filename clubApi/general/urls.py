from django.urls import path
from . import views

urlpatterns = [
    
    # Activity endpoints
    path('activities/', views.activity_list),
    path('activities/<int:pk>/', views.activity_detail),
    
    # Sponsor endpoints
    path('sponsors/', views.sponsor_list),
    path('sponsors/<int:pk>/', views.sponsor_detail),
]
