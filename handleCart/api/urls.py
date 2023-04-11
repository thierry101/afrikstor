from django.urls import path

from handleCart.api.views import CouponAPIView, OrderAPIView, OrderDetailView, UserClientAPIView


urlpatterns = [
    path('get-all-coupons/', CouponAPIView.as_view(), name='orders'),
    path('get-client-users/', UserClientAPIView.as_view(), name='userClient'),
    path('get-all-orders/', OrderAPIView.as_view(), name='userClient'),
    path('order-detail/<str:pk>/', OrderDetailView.as_view(), name="orderDetail"),
]
app_name = 'handleCartApi'
