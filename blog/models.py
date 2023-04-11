from django.db import models
from django_resized import ResizedImageField

from authentication.models import User

# Create your models here.


class modelBlog(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=200, blank=True, null=True)
    image = ResizedImageField(
        size=[500, 300], upload_to='Images/BlogCover', null=True, blank=True)
    author = models.CharField(max_length=200, blank=True, null=True)
    blogMsg = models.TextField(null=True, blank=True)
    statut = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)


class CommentBlog(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    blog = models.ForeignKey(
        modelBlog, on_delete=models.CASCADE, null=True, blank=True)
    subject = models.CharField(max_length=255, null=True, blank=True)
    statut = models.BooleanField(default=True)
    message = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)


class FAQ(models.Model):
    question = models.CharField(max_length=255, blank=True, null=True)
    answer = models.TextField(null=True, blank=True)
    availability = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self) -> str:
        return self.question
