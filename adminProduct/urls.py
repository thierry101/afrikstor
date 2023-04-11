from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('adminProduct.api.urls', namespace='apiAdmProd'))
]
app_name = 'api'
