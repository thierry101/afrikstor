from django.urls import path

from adminProduct.api.views import *


urlpatterns = [
    path('category/', CategoryAPIView.as_view(), name='category'),
    path('category/<int:pk>/', CategoryDetailView.as_view(), name="categoryDetail"),
    path('sub-category/', SubCategoryAPIView.as_view(), name='category'),
    path('sub-category/<int:pk>/', SubCategoryDetailView.as_view(),
         name="subCategoryDetail"),
    path('size/', SizeAPIView.as_view(), name='size'),
    path('size/<int:pk>/', SizeDetailView.as_view(), name="sizeDetail"),
    path('brand/', BrandAPIView.as_view(), name='brand'),
    path('brand/<int:pk>/', BrandDetailView.as_view(), name="brandDetail"),
]
app_name = "adminProduct"
