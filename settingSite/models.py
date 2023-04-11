from django.db import models
from django.utils import timezone
from PIL import Image
from django.core.files import File
from io import BytesIO
from django_resized import ResizedImageField


# Create your models here.


class SettingSite(models.Model):
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    orangeNber = models.CharField(
        'Numero orange', max_length=15, null=True, blank=True)
    localisation = models.CharField(max_length=255, blank=True, null=True)
    link_whatsapp = models.CharField(max_length=255, blank=True, null=True)
    link_whatsapp_grpe = models.CharField(
        max_length=255, blank=True, null=True)
    link_facebook = models.CharField(max_length=255, blank=True, null=True)
    link_instagram = models.CharField(max_length=255, blank=True, null=True)
    link_messenger = models.CharField(max_length=255, blank=True, null=True)
    mtnMoney = models.CharField(max_length=15, null=True, blank=True)
    orangeMoney = models.CharField(max_length=15, null=True, blank=True)
    ourSlogan = models.CharField(max_length=255, null=True, blank=True)
    nameSite = models.CharField(max_length=255, default='allAfrik')
    logo = ResizedImageField(
        size=[500, 300], upload_to='Images/SettingSites', null=True, blank=True)
    fav_icon = ResizedImageField(
        size=[500, 300], upload_to='Images/SettingSites', null=True, blank=True)
    state = models.BooleanField(default=True)


class ConfidentialityAndRule(models.Model):
    confidentiality = models.TextField(null=True, blank=True)
    rulerSeller = models.TextField(null=True, blank=True)
    rulerBuyer = models.TextField(null=True, blank=True)


class Visitor_Infos(models.Model):
    ip_address = models.GenericIPAddressField()
    page_visited = models.TextField()
    event_date = models.DateTimeField(timezone.now())

    def __str__(self) -> str:
        return self.ip_address
