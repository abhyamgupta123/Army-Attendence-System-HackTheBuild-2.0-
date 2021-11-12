from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    uid = models.CharField(max_length = 50, unique = True, blank = False)
    # attendence_string = models.CharField(max_length = 365, unique = False)