from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=128)  # Store hashed passwords

    def __str__(self):
        return self.username

class Places(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='places')
    name = models.CharField(max_length=255)
    description = models.TextField()    
    location = models.CharField(max_length=255)
    image_url_1 = models.URLField(max_length=500, blank=True, null=True)
    image_url_2 = models.URLField(max_length=500, blank=True, null=True)
    image_url_3 = models.URLField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class Location(models.Model):
    place = models.ForeignKey(Places, on_delete=models.CASCADE, related_name='locations')
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"Location of {self.place.name}: ({self.latitude}, {self.longitude})"