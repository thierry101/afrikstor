from rest_framework import serializers
from adminProduct.api.serializers import BrandSerializer

from provider.models import Provider


class ProviderSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()

    class Meta:
        model = Provider
        fields = '__all__'
