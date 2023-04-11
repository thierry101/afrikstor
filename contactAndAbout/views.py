from django.http import JsonResponse
from django.shortcuts import render

from backend.regex import checkLenOfField, checkPhoneError, setEmailError
from contactAndAbout.models import AboutUs, MessageContact

# Create your views here.


def indexAbout(request):
    aboutUs = AboutUs.objects.filter(available=True).first()
    context = {
        'aboutUs': aboutUs
    }

    return render(request, 'contactAbout/about.html', context)


def indexMessage(request):
    context = {
        'message': True
    }
    return render(request, 'contactAbout/contact.html', context)


def receivedMessage(request):
    name = ''
    surname = ''
    email = ''
    phone = ''
    errors = {}
    if request.method == 'POST' and request.is_ajax():
        data = request.POST
        message = checkLenOfField('message', data['message'], 5, errors)
        if not request.user.is_authenticated:
            name = checkLenOfField('name', data['name'], 2, errors)
            surname = checkLenOfField('surname', data['surname'], 2, errors)
            email = setEmailError('email', data['email'], errors)
            phone = checkPhoneError('phone', data['phone'], errors)
        if len(errors) == 0:
            if request.user.is_authenticated:
                messageSend = MessageContact.objects.create(
                    user_id=request.user.id, message=message)
                messageSend.save()
            else:
                messageSend = MessageContact.objects.create(
                    name=name, surname=surname, email=email, message=message, phone=phone)
                messageSend.save()
            return JsonResponse('success', status=200, safe=False)
        else:
            return JsonResponse(errors, status=400, safe=False)
