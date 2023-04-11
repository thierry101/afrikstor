from rest_framework.serializers import ModelSerializer
from authentication.api.serializers import UserSerializer
from contactAndAbout.models import MessageContact


class MessageSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = MessageContact
        fields = '__all__'
