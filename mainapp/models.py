from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    age = models.IntegerField(null=True,blank=True, default=None)


class Item(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    overview = models.CharField(max_length=2000, null=True)
    prepration = models.CharField(max_length=2000, null=True)
    price = models.CharField(max_length=200, null=True)
    age_group= models.CharField(max_length=10, blank=True, null=True)
    duration= models.CharField(max_length=2000, null=True)
    done = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name