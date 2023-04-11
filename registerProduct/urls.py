from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('registerProduct.api.urls', namespace='apiRegistrProduct'))
]
app_name = 'api'
