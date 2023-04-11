from django.contrib import admin
from django.urls import path

from provider.api.views import ProviderAPIView, ProviderDetailView


urlpatterns = [
    path('provider/', ProviderAPIView.as_view(), name='provider'),
    path('provider/<int:pk>/', ProviderDetailView.as_view(), name="providerDetail"),
]
app_name = "provider"
