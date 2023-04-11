from django.db import models
from authentication.models import User

from registerProduct.models import RegisterProduct

# Create your models here.


class CommentProduct(models.Model):
    product = models.ForeignKey(
        RegisterProduct, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
