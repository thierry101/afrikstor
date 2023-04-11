from django.db import models
from authentication.models import User
from registerProduct.models import RegisterProduct
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.


class OrderItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey(
        RegisterProduct, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=50, null=True, blank=True)
    price = models.CharField(max_length=50, blank=True, null=True)
    pathImg = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(default=1)
    total = models.DecimalField(
        max_digits=100, decimal_places=2, blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    # order = models.ForeignKey(
    #     'Order', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.quantity} of {self.product.title}"


class Order(models.Model):
    # si je veux qu'un user anonyme puisse commander je dois ajouter la valeur null et blank dans user
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    items = models.ManyToManyField(OrderItem, blank=True)
    address = models.ForeignKey(
        'ShippingAdress', on_delete=models.CASCADE, null=True, blank=True)
    paymentMethod = models.CharField(max_length=255, null=True, blank=True)
    nberInvoice = models.CharField(
        max_length=10, null=True, blank=True, unique=True)
    orderNumber = models.CharField(
        max_length=20, null=True, blank=True, unique=True)
    # start_date = models.DateTimeField(auto_now_add=True)
    # ordered_date = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    status = models.CharField(max_length=20, default='ouvert')
    # payement_complete = models.BooleanField(default=False)
    reduction = models.DecimalField(
        max_digits=100, default=0.00, decimal_places=2)
    newTotal = models.DecimalField(
        max_digits=100, default=0.00, decimal_places=2)
    infoAnonUser = models.TextField(null=True, blank=True)
    commandProducts = models.TextField(null=True, blank=True)
    priceDelivery = models.FloatField(default=0)
    delivered = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    # def __str__(self) -> str:
    #     if self.user:
    #         return self.nberInvoice
    #         # return f"{self.user.first_name} command complete {self.complete}"
    #     else:
    #         return self.nberInvoice
    # return 'anonymoususer for command No : ' + self.orderNumber


class CouponGerate(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    code = models.CharField(max_length=15, unique=True)
    valid_from = models.DateField()
    valid_to = models.DateField()
    discount = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)])
    active = models.BooleanField(default=False)


class ShippingAdress(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    surname = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    situation = models.CharField(max_length=100, null=True, blank=True)
    default = models.BooleanField(default=False)

    # def __str__(self):
    #     return self.name + ' ' + self.surname
