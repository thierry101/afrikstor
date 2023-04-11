from django.contrib import admin
from django.urls import path

from registerProduct.api.views import GetAllProductsAPIView, GetAllProductsEditAPIView, RegisterProductAPIView, RegisterProductDetailView


urlpatterns = [
    path('register-product/', RegisterProductAPIView.as_view(), name='regisProd'),
    path('get-all-products/', GetAllProductsAPIView.as_view(), name='getAllProds'),
    path('get-all-products/<int:pk>/',
         GetAllProductsEditAPIView.as_view(), name='getAllProdsEdit'),
    path('edit-delete-product/<int:pk>/',
         RegisterProductDetailView.as_view(), name="prodDetail"),
]
app_name = "regisProd"
