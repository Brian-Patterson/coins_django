from email.policy import default
from operator import truediv
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Coins(models.Model):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=250)
    material = models.CharField(max_length=100)
    origin = models.CharField(max_length=100)
    weight = models.CharField(max_length=100)
    year = models.IntegerField(default=0)
    history = models.TextField(max_length=500)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Owner(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=250)
    asking_price = models.IntegerField(default=0)
    coins = models.ForeignKey(Coins, on_delete=models.CASCADE, related_name="owners", null=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    title = models.CharField(max_length=150)
    coins = models.ManyToManyField(Coins)

    def __str__(self):
        return self.title