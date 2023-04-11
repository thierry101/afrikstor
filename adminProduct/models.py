from django.db import models
from django_resized import ResizedImageField

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True, unique=True)
    # image = ResizedImageField(
    #     size=[500, 300], upload_to='products/category', null=True, blank=True)
    # description = models.TextField(blank=True, null=True)
    statut = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self) -> str:
        return self.name


class SubCategory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True, unique=True)
    image = ResizedImageField(
        size=[500, 300], upload_to='products/subCategory', null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    statut = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self) -> str:
        return self.name + 'sub-category of  ' + self.category.name


class Size(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, unique=True)
    statut = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self) -> str:
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True, unique=True)
    description = models.TextField(blank=True, null=True)
    statut = models.BooleanField(default=True)
    image = ResizedImageField(
        size=[500, 300], upload_to='products/Brand', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self) -> str:
        return self.name
