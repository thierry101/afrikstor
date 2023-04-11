from django.urls import path, include

from handleCart.views import AddToCart, applyCoupon, checkoutIndex, closeOrder, confirmOrder, delItemFromOrder, registerAddress, updateQte, viewCart
# from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('api/', include('handleCart.api.urls', namespace='cartHandle')),
    path('add-to-cart/', AddToCart, name='addCart'),
    path('view-cart/', viewCart, name='viewCart'),
    path('update-quantity-item/', updateQte, name='updateQte'),
    path('delete-item-from-order/', delItemFromOrder, name='delItem'),
    path('checkout/', checkoutIndex, name='checkout'),
    path('apply-discount/', applyCoupon, name='discount'),
    path('register-address/', registerAddress, name='address'),
    path('confirm-order/', confirmOrder, name='confirmAdr'),
    path('close-order/<str:id>/', closeOrder, name='homendex'),
]
app_name = 'handleCart'
