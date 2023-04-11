from django.contrib import admin
from django.urls import path

from settingSite.api.views import ConfidentialityAndRuleAPIView, GetConfidentialityAndRuleAPIView, SettingSiteAPIView


urlpatterns = [
    path('setting-site/', SettingSiteAPIView.as_view(), name='reset'),
    path('get-confidentiality-rules/',
         GetConfidentialityAndRuleAPIView.as_view(), name='getRulConfid'),
    path('confidentiality-rules/',
         ConfidentialityAndRuleAPIView.as_view(), name='confidRul'),
]
app_name = "settingSit"
