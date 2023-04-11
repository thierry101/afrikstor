from rest_framework import serializers
from settingSite.models import *


class SettingSiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SettingSite
        fields = '__all__'


class ConfidentialityAndRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfidentialityAndRule
        fields = '__all__'
