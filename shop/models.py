from django.db import models

from authentication.models import User
from registerProduct.models import RegisterProduct

# Create your models here.


class Wishlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(
        RegisterProduct, on_delete=models.CASCADE, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
