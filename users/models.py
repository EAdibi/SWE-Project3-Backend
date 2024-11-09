from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    # AbstractUser is a built-in Django model that provides a lot of the functionality we need for a user
    # So here we'll just add some additional information that we may or may not use
    bio = models.TextField(null=True, blank=True, max_length=500)
    google_id = models.CharField(max_length=255, null=True, blank=True)
