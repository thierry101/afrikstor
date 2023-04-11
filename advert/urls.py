from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('advert.api.urls', namespace='apiAdvert'))
]
app_name = 'api'
