from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from random import randint
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image

# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable=False)
    account_balance = models.FloatField(default=0);
    mykad = models.CharField(max_length=14, null=True, unique=True)
    profesion = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=15, null=True)
    address = models.CharField(max_length=50, null=True)
    postcode = models.CharField(max_length=7, null=True)
    city = models.CharField(max_length=20, null=True)
    country = models.CharField(max_length=20, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(default='default.png', upload_to='profile_pic')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height>200 or img.width>200:
            output_size=(200,200)
            img.thumbnail(output_size)
            img.save(self.image.path)


