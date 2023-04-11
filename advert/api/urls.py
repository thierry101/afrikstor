from django.urls import path

from advert.api.views import AdvertAPIView, AdvertEditAPIView


urlpatterns = [
    path('show-add-advert/', AdvertAPIView.as_view(), name="shAddBrand"),
    path('show-add-advert/<int:pk>/',
         AdvertEditAPIView.as_view(), name="editAdvert"),
]
app_name = "advert"
