from django.db import models
from rest_framework.authtoken.admin import User


# Create your models here.
class UserProfile(User):
    close_friends = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __str__(self):
        return self.username
