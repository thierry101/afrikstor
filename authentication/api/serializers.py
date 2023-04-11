from rest_framework.serializers import ModelSerializer
from adminProduct.api.serializers import BrandSerializer
from authentication.models import User


class UserSerializer(ModelSerializer):
    brand = BrandSerializer()

    class Meta:
        model = User

        fields = ['id', 'first_name', 'last_name',
                  'email', 'role', 'statut', 'image', 'phone', 'brand', 'country', 'city', 'accountMoney']
