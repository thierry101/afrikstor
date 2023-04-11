from rest_framework.serializers import ModelSerializer
from adminProduct.api.serializers import BrandSerializer, CategorySerializer, SizeSerializer, SubCategorySerializer
from authentication.api.serializers import UserSerializer

from registerProduct.models import RegisterProduct


class RegisterProductSerializer(ModelSerializer):
    user = UserSerializer()
    category = CategorySerializer()
    subCategory = SubCategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    sizes = SizeSerializer(read_only=True, many=True)

    class Meta:
        model = RegisterProduct

        fields = '__all__'
