from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(blank=False, null=False, unique=True)
    name = models.CharField(max_length=128, unique=False)
    username = models.CharField(max_length=128, unique=False)
    about = models.TextField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        if self.username is None:
            self.username = (self.first_name[0] + self.last_name.replace(' ', '')).lower()
        super().save(*args, **kwargs)


class Location(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)

    def __str__(self):
        return self.address


class EmergencyService(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class EmergencyVehicle(models.Model):
    service = models.ForeignKey(EmergencyService, on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=20)
    current_location = models.ForeignKey(Location, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.service.name} - {self.vehicle_number}"


class Route(models.Model):
    name = models.CharField(max_length=100)
    start_location = models.ForeignKey(Location, related_name='start_location', on_delete=models.CASCADE)
    end_location = models.ForeignKey(Location, related_name='end_location', on_delete=models.CASCADE)
    waypoints = models.ManyToManyField(Location, related_name='route_waypoints')

    def __str__(self):
        return self.name


class EmergencyCall(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    caller_name = models.CharField(max_length=100)
    caller_contact = models.CharField(max_length=20)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    emergency_service = models.ForeignKey(EmergencyService, on_delete=models.CASCADE)
    assigned_vehicle = models.ForeignKey(EmergencyVehicle, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')])

    def __str__(self):
        return f"{self.caller_name} - {self.emergency_service.name}"


class ServerlessApp(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    access_url = models.CharField(max_length=512)
    docker_image = models.CharField(max_length=512)
    status = models.CharField(max_length=20, choices=[('Development', 'Development'), ('Staging', 'Staging'), ('Production', 'Production')])

    def __str__(self):
        return self.name


class Event(models.Model):
    event_name = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    organizer_name = models.CharField(max_length=255)

    def __str__(self):
        return self.event_name