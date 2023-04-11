import random
import string
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django_resized import ResizedImageField

from adminProduct.models import Brand
# Create your models here.


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    first_name = models.CharField(
        'Prenom', max_length=255, null=True, blank=True)
    last_name = models.CharField('Nom', max_length=255, null=True, blank=True)
    email = models.CharField(
        max_length=255, blank=True, null=True, unique=True)
    role = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    accountMoney = models.CharField(
        max_length=15, null=True, blank=True)
    image = ResizedImageField(
        size=[500, 300], upload_to='Images/Profiles', null=True, blank=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, blank=True, null=True)
    nameShop = models.CharField(max_length=255, null=True, blank=True)
    # logoShop = models.ImageField(
    #     upload_to='Images/LogoShop', null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    statut = models.BooleanField(default=False, blank=True, null=True)
    approve = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(
        default=False, blank=True, null=True)
    username = None
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self) -> str:
        return self.email

    objects = CustomUserManager()


class UserToken(models.Model):
    user_id = models.IntegerField()
    token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()


class Reset(models.Model):
    email = models.CharField(max_length=255)
    token = models.CharField(max_length=255, unique=True)


def generate_activation_code():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(6))


class ActivationCode(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    code = models.CharField(max_length=6, default=generate_activation_code)
