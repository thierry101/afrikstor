from rest_framework import serializers
from adminProduct.api.serializers import BrandSerializer

from advert.models import Advert


class AdvertSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = Advert
        fields = '__all__'
