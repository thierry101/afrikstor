from django.urls import path

from contactAndAbout.api.views import MessageAPIView, MessageDetailView


urlpatterns = [
    # path('order-detail/<int:pk>/', OrderDetailView.as_view(), name="orderDetail"),
    path('retrieve-message/', MessageAPIView.as_view(), name='getAllMsg'),
    path('update-message/<int:pk>/', MessageDetailView.as_view(), name='updateMsg'),
]
app_name = 'handleContactApi'
