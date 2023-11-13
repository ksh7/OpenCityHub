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


class Event(models.Model):
    event_name = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    organizer_name = models.CharField(max_length=255)

    def __str__(self):
        return self.event_name