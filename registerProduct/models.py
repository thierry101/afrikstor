from django.db import models
from adminProduct.models import *
from authentication.models import User
from django_resized import ResizedImageField

# Create your models here.


class RegisterProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, related_name='registerProduct', on_delete=models.CASCADE, blank=True, null=True)
    subCategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, blank=True, null=True)
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    price = models.DecimalField(
        default=0.00, max_digits=100, decimal_places=2, null=True, blank=True)
    sold_price = models.DecimalField(
        default=0.00, max_digits=100, decimal_places=2, null=True, blank=True)
    mainImg = ResizedImageField(
        size=[500, 300], upload_to='products/Mains_Images', null=True, blank=True)
    secondImg = ResizedImageField(
        size=[500, 300], upload_to='products/Mains_Images', null=True, blank=True)
    othersImgs = ResizedImageField(
        size=[500, 300], upload_to='products/Others_images', null=True, blank=True)
    colorsImgs = ResizedImageField(
        size=[500, 300], upload_to='products/Others_images', null=True, blank=True)
    colors = models.TextField(null=True, blank=True)
    sizes = models.ManyToManyField(Size, blank=True)
    tabOtherImgs = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    availability = models.BooleanField(default=True)
    validateProd = models.BooleanField(default=False)
    rate = models.DecimalField(
        default=0.00, max_digits=100, decimal_places=2, null=True, blank=True)
    colorimgs = models.TextField(null=True, blank=True)
    rejectReason = models.TextField(null=True, blank=True)
    # sizeVariation = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ['price']

    def __str__(self) -> str:
        return self.title

    def get_pourcentage(self):
        return 100 - round(self.sold_price / self.price * 100)

    @property
    def get_photo_url(self):
        # print('main img', self.mainImg)
        # print('second image', self.secondImg)
        if self.secondImg and hasattr(self.secondImg, 'url'):
            return self.secondImg.url
        else:
            pass
