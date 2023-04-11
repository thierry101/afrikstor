from django.urls import path
from home.processor import save_visitor_infos

from home.views import commentsProduct, detailProduct, indexHome, showProductSByBrands

urlpatterns = [
    path('', indexHome, name='homeIndex'),
    path('product-detail/<int:id>/', detailProduct, name='detailProd'),
    path('products-brand=<str:brand>/<int:id>/',
         showProductSByBrands, name='brandProds'),
    path('post-comment/', commentsProduct, name='commentProd'),
    path('count-visitors/', save_visitor_infos, name='countVisitor'),
]
app_name = 'homePath'
