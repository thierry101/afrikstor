from turtle import title
from django.db import models
from django_resized import ResizedImageField

from adminProduct.models import Brand

# Create your models here.


class Advert(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, blank=True, null=True)
    begin_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    img = ResizedImageField(
        size=[500, 300], upload_to='Banners/Adverts', null=True, blank=True)
    statut = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self) -> str:
        return self.title
