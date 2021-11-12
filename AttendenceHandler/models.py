from django.db import models
from django.contrib.auth.models import User


class Attendence(models.Model):

    user = models.ForeignKey(User, on_delete = models.CASCADE)
    month = models.DateTimeField()
    att_string = models.CharField(max_length = 365, unique = False)