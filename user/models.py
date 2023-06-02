


# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    is_admin= models.BooleanField('Is admin', default=False)
    is_technician = models.BooleanField('Is technician', default=False)
    is_customer_care = models.BooleanField('Is customer care', default=False)
    is_employe = models.BooleanField('Is employee', default=False)
    is_supervisor = models.BooleanField('Is supervisor', default=False)
    is_logged_in = models.BooleanField(default=False)
