from django.urls import path, include

from contactAndAbout.views import indexAbout, indexMessage, receivedMessage


urlpatterns = [
    path('api/', include('contactAndAbout.api.urls', namespace='mesgHandle')),
    path('about/', indexAbout, name='aboutIndex'),
    path('contact/', indexMessage, name='contactIndex'),
    path('send-message/', receivedMessage, name='sendMsg'),
]
app_name = 'contactAbout'
