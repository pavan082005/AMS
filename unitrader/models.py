from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    date_joined = models.DateField(auto_now_add=True)
    ph_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username
