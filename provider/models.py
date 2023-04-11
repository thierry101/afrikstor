from django.db import models
from django_resized import ResizedImageField

from adminProduct.models import Brand


# Create your models here.


class Provider(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    name_product = models.CharField(max_length=255, blank=True, null=True)
    surname = models.CharField(max_length=255, blank=True, null=True)
    entreprise = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    image = ResizedImageField(
        size=[500, 300], upload_to='Providers/ImagesProducts', null=True, blank=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, blank=True, null=True)
    state = models.CharField(max_length=255, blank=True, null=True)
    statut = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self) -> str:
        return self.name
