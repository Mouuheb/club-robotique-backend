from django.db import models
from django.conf import settings
from django.utils import timezone

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='api_groups',
        blank=True
    )

    def __str__(self):
        return self.name
    

class Task(models.Model):
    title = models.CharField(max_length=200)
    deadline = models.DateTimeField()
    xp = models.PositiveIntegerField(default=10)
    description = models.TextField(blank=True, null=True)
    category = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_tasks'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateTimeField()
    location = models.TextField()
    description = models.TextField(blank=True, null=True)
    image_link = models.TextField(blank=True, null=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='events_attending',
        blank=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_events'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title