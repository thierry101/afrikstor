from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('provider.api.urls', namespace='apiProvider'))
]
app_name = 'api'
