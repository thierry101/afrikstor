from django.urls import path

from authentication.api.views import *

urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login'),
    # path('two-factor/', TwoFactorAPIView.as_view(), name='twoFactor'),
    path('register/', RegisterAPIVIew.as_view(), name='register'),
    path('register-seller/', RegisterSellerAPIVIew.as_view(), name='registerSeller'),
    path('user/', UserAPIView.as_view(), name='user'),
    path('refresh/', RefreshAPIView.as_view(), name='refresh'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('forgot/', ForgotAPIView.as_view(), name='forgot'),
    path('reset/', ResetAPIView.as_view(), name='reset'),
    path('register/<int:pk>/', RegisterDetailAPIView.as_view(),
         name="registerDetail"),
    path('activate-user/<code>/', checkActivationCode, name='activate'),
]
app_name = "auth"
