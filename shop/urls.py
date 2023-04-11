from django.contrib import admin
from django.urls import path, include

from shop.views import ListProducts, apiWishlist, listProducts, removeItemWishlist, suggestionApi, wishlist
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    # path('shop', ShopIndex, name='shopIndex'),
    path('shop/', listProducts, name='shopIndex'),
    # path('shop/', filterArticle, name='filterProds'),
    path('api-suggestion/', csrf_exempt(suggestionApi), name='sugrProds'),
    path('add-wishlist/', apiWishlist, name='apiWishlist'),
    path('wishlist/', wishlist, name='wishlist'),
    path('delete-item-wishlist/', removeItemWishlist, name='delItemWish'),
]
app_name = 'shopPath'
