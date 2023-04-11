from django.db import models
from django_resized import ResizedImageField

from authentication.models import User

# Create your models here.


class MessageContact(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    surname = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    statut = models.CharField(max_length=15, default='non lu')
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)


class AboutUs(models.Model):
    smallMessage = models.TextField(null=True, blank=True)
    freeDelivry = models.CharField(max_length=255, null=True, blank=True)
    signature = ResizedImageField(
        size=[500, 300], upload_to='Signatures', null=True, blank=True)
    available = models.BooleanField(default=True)
