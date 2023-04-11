from rest_framework.serializers import ModelSerializer
from authentication.api.serializers import UserSerializer

from handleCart.models import CouponGerate, Order, ShippingAdress


# class OrderSerializer(ModelSerializer):
#     user = UserSerializer()

#     class Meta:
#         model = Order
#         fields = '__all__'


class CouponSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = CouponGerate
        fields = '__all__'


class ShippingAdressSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = ShippingAdress
        fields = '__all__'


class OrderSerializer(ModelSerializer):
    user = UserSerializer()
    address = ShippingAdressSerializer()

    class Meta:
        model = Order
        fields = '__all__'
