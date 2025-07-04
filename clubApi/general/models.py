from django.db import models

class Activity(models.Model):
    img = models.TextField(verbose_name="Image URL")
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    link = models.TextField(verbose_name="Sponsor URL")
    img = models.TextField(verbose_name="Logo URL")

    def __str__(self):
        return self.name