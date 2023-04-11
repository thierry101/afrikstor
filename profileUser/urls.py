from django.urls import path

from profileUser.views import EditProfile, getCommand, indexProfile, reserPassword


urlpatterns = [
    path('profile/', indexProfile, name='profileIndex'),
    path('edit-profile/', EditProfile, name='editprofileIndex'),
    path('reset/<str:token>/', reserPassword, name='showTemplPassw'),
    path('get-order/<str:pk>/', getCommand, name="getOrder"),
]
app_name = 'profile'
