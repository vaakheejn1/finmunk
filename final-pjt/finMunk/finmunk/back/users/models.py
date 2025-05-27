# back/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
# from products.models import DepositProduct,SavingProduct

class User(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    job = models.BooleanField(default=False)
    income = models.PositiveIntegerField(null=True, blank=True)
    assets = models.PositiveIntegerField(null=True, blank=True)

    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='followings', blank=True)
    bio = models.CharField(max_length=100, blank=True, null=True, verbose_name="자기소개")

    def __str__(self):
        return self.username
