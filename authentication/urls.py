from django.contrib import admin
from django.urls import path, include
# from django.views.decorators.csrf import csrf_exempt

from authentication.views import confiDataTempl, loginUser, logoutUser, rulerBuyer, templateLogin

urlpatterns = [
    path('api/', include('authentication.api.urls', namespace='apiAuth')),
    path('login/', templateLogin, name='loginTempl'),
    path('logout/', logoutUser, name='logout'),
    path('login-user/', loginUser, name='login'),
    path('data-confidentiality/', confiDataTempl, name='confidData'),
    path('ruler-for-buyer/', rulerBuyer, name='buyerRuler'),
]
app_name = 'api'
